# Generated by Django 4.2.5 on 2023-09-22 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locationdevoiture', '0002_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='photo',
            field=models.CharField(default='', max_length=3000),
        ),
    ]