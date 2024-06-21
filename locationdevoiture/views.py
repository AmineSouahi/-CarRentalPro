from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseServerError
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from .models import car,Reservation
from .models import CustomUser
from datetime import timedelta
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    cars = car.objects.all()[:5]
    return render(request, 'home.html', {'cars' : cars})

def user_login(request):
    if request.method == 'POST':
        email_or_username = request.POST['email_or_username']
        password = request.POST['password']

        # Authenticate the user using the custom backend
        user = authenticate(request, username=email_or_username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')  # Redirect to the home page after login
            else:
                messages.error(request, 'Your account is inactive.')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            # Check if a user with the same email or username already exists
            if CustomUser.objects.filter(email=email).exists() or CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'A user with this email or username already exists.')
            else:
                # Create the custom user
                user_obj = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name,
                )

                # Log the user in
                user = authenticate(request, username=username, password=password1)
                if user is not None:
                    login(request, user)
                    return redirect('home')  # Redirect to the home page after signup
                else:
                    messages.error(request, 'Failed to log in after signup.')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'signup.html')


def reservation(request, car_id):
    cars = get_object_or_404(car, pk=car_id)
    user = request.user  # Assuming you have authentication enabled

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        reservation_prise = request.POST.get('reservation_prise')
        reservation_retour = request.POST.get('reservation_retour')

        # Create a new Reservation object and set the payment_status to "Pending"
        reservation = Reservation(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            date_de_prise=reservation_prise,
            date_de_retour=reservation_retour,
            car_name=cars.name,
            payment_status='Pending',
            # Set payment_status to "Pending"
        )

        reservation.save()

        messages.success(request, 'Votre réservation a été enregistrée avec succès!')

        # Now that the reservation is created, you can get its ID
        reservation_id = reservation.id

        # Redirect to the payment page and pass both car_id and reservation_id
        return redirect('payment', car_id=cars.id, reservation_id=reservation_id)

    return render(request, 'reservation.html', {'cars': cars})

def detaille(request, car_id):
    cars = get_object_or_404(car, pk=car_id)
    return render(request, 'detaille.html', {'cars':cars})


@login_required
def reservation_list(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user)
    return render(request, 'reservation_list.html', {'reservations': reservations})

def custom_logout(request):
    logout(request)
    return redirect('home')

def send_email_to_client(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)

        subject = 'Your Reservation Details'
        message = f"Hello {reservation.first_name},\n\nThank you for your reservation. Here are the details:\n\nFirst Name: {reservation.first_name}\nLast Name: {reservation.last_name}\nReservation Date and Time: {reservation.reservation_datetime}\n\nWe look forward to serving you!\n\nBest regards,\nYour Company Name"

        # Use the send_mail function to send the email
        send_mail(
            subject,
            message,
            'zikossezm@gmail.com',
            [reservation.email],  # Use the client's email here
            fail_silently=False,
        )

        return HttpResponse('Email sent successfully')
    except Reservation.DoesNotExist:
        return HttpResponse('Reservation not found', status=404)
    except Exception as e:
        return HttpResponse(f'An error occurred: {str(e)}', status=500)


def process_payment(request, car_id, reservation_id):
    cars = get_object_or_404(car, pk=car_id)
    res = get_object_or_404(Reservation, pk=reservation_id)
    reservation_duration = res.date_de_retour - res.date_de_prise

    # Convert the duration to days (or any other appropriate unit)
    # Assuming you want the duration in days
    total_days = reservation_duration.days

    # Calculate the total price based on the number of days and car price
    total = total_days * cars.prix

    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiration_date = request.POST.get('expiration_date')
        cvv_code = request.POST.get('cvv_code')
        name_on_card = request.POST.get('name_on_card')

        # Validate the credit card details
        if is_valid_credit_card(card_number):
            # Assuming you have a function is_valid_credit_card to validate the credit card

            # Update the reservation's payment_status to "Paid"
            reservation = get_object_or_404(Reservation, pk=reservation_id)
            reservation.payment_status = 'Paid'
            reservation.save()

            # Calculate total here, as this is part of the successful payment flow


            # Add your payment processing logic here
            # For example, you can use a payment gateway API to process payments

            # After processing the payment, you can redirect to a success page
            success_message = "Payment succeeded. Thank you for your reservation!"
            failed_message = "Payment failed. !"

            # Return an HTTP response with the success message
            messages.success(request, 'Votre Paiement a été enregistrée avec succès!')

        else:
            messages.error(request, "Votre Paiement n'a pas  été enregistrée avec succès!")

    return render(request, 'payment.html', {'cars': cars, 'total': total})


def is_valid_credit_card(card_number):
    card_number = card_number.replace(" ", "")  # Remove spaces from the card number
    if not card_number.isdigit():
        return False

    card_digits = [int(digit) for digit in card_number]
    card_digits.reverse()

    doubled_digits = [2 * digit if idx % 2 == 1 else digit for idx, digit in enumerate(card_digits)]
    summed_digits = [digit - 9 if digit > 9 else digit for digit in doubled_digits]

    total = sum(summed_digits)

    return total % 10 == 0