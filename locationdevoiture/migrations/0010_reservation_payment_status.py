# Generated by Django 4.2.5 on 2023-09-23 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locationdevoiture', '0009_reservation_user_alter_customuser_expiration_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='payment_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending', max_length=10),
        ),
    ]
