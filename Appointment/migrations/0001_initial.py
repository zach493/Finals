# Generated by Django 5.0.4 on 2024-05-19 18:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment_resident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('mobile_number', models.CharField(max_length=11)),
                ('permanent_address', models.TextField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FinishedAppointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('request', models.TextField(blank=True)),
                ('service_id', models.TextField(blank=True)),
                ('sent_date', models.DateField(auto_now_add=True)),
                ('rejected_date', models.DateField(auto_now_add=True)),
                ('appointment_date', models.DateField(blank=True, null=True)),
                ('appointment_time', models.TimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Guardian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('age', models.CharField(max_length=100)),
                ('middle_name', models.CharField(max_length=100)),
                ('permanent_address', models.CharField(max_length=100)),
                ('other_concerns', models.CharField(max_length=254)),
                ('date_of_birth', models.DateField()),
                ('service_id', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('mobile_number', models.CharField(max_length=11)),
                ('permanent_address', models.TextField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Resident',
                'verbose_name_plural': 'Residents',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('Description', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='service_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='service_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('phone', models.CharField(max_length=50)),
                ('request', models.TextField(blank=True)),
                ('service_id', models.TextField(blank=True, max_length=50)),
                ('sent_date', models.DateField(auto_now_add=True)),
                ('accepted', models.BooleanField(default=False)),
                ('accepted_date', models.DateField(blank=True, null=True)),
                ('appointment_date', models.DateField(auto_now_add=True, null=True)),
                ('appointment_time', models.TimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-sent_date'],
            },
        ),
        migrations.CreateModel(
            name='ConcreteAppointmentResident',
            fields=[
                ('appointment_resident_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Appointment.appointment_resident')),
                ('groups', models.ManyToManyField(blank=True, related_name='app_users_groups', to='auth.group', verbose_name='groups')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_resident', to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='app_users_permissions', to='auth.permission', verbose_name='user permissions')),
            ],
            bases=('Appointment.appointment_resident',),
        ),
    ]
