from django.contrib import admin
from django.core.mail import send_mail
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.template.loader import render_to_string
from django.urls import reverse
from .models import car,Reservation

class CustomUserAdmin(UserAdmin):
    list_display = ('id','username', 'email', 'first_name', 'last_name', 'credit_card', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'credit_card')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Add other configurations as needed

admin.site.register(CustomUser, CustomUserAdmin)


class ReservationAdmin(admin.ModelAdmin):
    def get_user_id(self, obj):
        return obj.user.id

    get_user_id.short_description = 'User ID'
    list_display = ('id','first_name', 'last_name', 'email', 'phone_number', 'date_de_prise','date_de_retour','car_name', 'send_email_link', 'get_user_id')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('date_de_prise','date_de_retour')
    def send_email_link(self, obj):
        email_url = reverse('send_email_to_client', args=[obj.id])
        return format_html('<a class="button" href="{}">Send Email</a>', email_url)

    send_email_link.short_description = "Send Email to Client"

    actions = ['send_selected_emails']

    def send_selected_emails(modeladmin, request, queryset):
        # Loop through the selected reservations and send emails
        for reservation in queryset:
            # Use the send_mail function to send emails
            send_mail(
                'Subject',
                'Message',
                'from@example.com',
                [reservation.email],  # Use the client's email here
                fail_silently=False,
            )
            # Optionally, you can update the reservation object to mark it as emailed

    send_selected_emails.short_description = "Send selected emails"

admin.site.register(Reservation, ReservationAdmin)

def send_selected_emails(modeladmin, request, queryset):
    for reservation in queryset:
        # Load and render the email template
        email_message = render_to_string('email_templates/reservation_email.html', {
            'first_name': reservation.first_name,
            'last_name': reservation.last_name,
            'email': reservation.email,
            'phone_number': reservation.phone_number,
            'reservation_datetime': reservation.reservation_datetime,

        })

        # Use the email_message in the send_mail function to send the email
        send_mail(
            'Reservation Confirmation',
            
            
            email_message,
            'zikossezm@gmail.com',
            [reservation.email],  # Use the client's email here
            fail_silently=False,
        )


class CarAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'annee', 'color', 'modele', 'description')





admin.site.register(car, CarAdmin)