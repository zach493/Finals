# Generated by Django 5.0.4 on 2024-05-20 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment', '0009_alter_appointment_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='guardian',
            name='request',
            field=models.TextField(blank=True, max_length=100),
        ),
    ]
