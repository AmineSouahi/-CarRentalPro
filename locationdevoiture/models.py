#models.py

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings



class CustomUser(AbstractUser):
    credit_card = models.CharField(max_length=16, blank=True, null=False, default="12345678910111214")
    phone_number = models.CharField(max_length=15, blank=True, null=True, default="12345678910111214")
    cvc = models.IntegerField(max_length=3, blank=True, null=False, default="123")
    expiration_date = models.DateField(default='2023-07-23')
    card_name = models.CharField(max_length=100,default="")
    groups = models.ManyToManyField(Group, blank=True, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='customuser_set')




class car(models.Model):

    name=models.CharField(max_length=50,default="car")
    annee = models.IntegerField(default=0)
    modele=models.CharField(max_length=50,default="xxxx")
    photo = models.CharField(max_length=3000,default="")
    prix = models.FloatField(default=00.00)
    description = models.CharField(max_length=1000,default='')
    color = models.CharField(max_length=50, default="")


User = get_user_model()

class Reservation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Use the custom user model
        on_delete=models.CASCADE,
        default=1  # Set the default user ID here
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    date_de_prise = models.DateTimeField()
    date_de_retour = models.DateTimeField()
    car_name=models.CharField(max_length=100)
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ]

    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending',
    )


