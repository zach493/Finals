from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,Group, Permission, User
from django.utils.translation import gettext_lazy as _

# register
class BaseUser(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=11)
    permanent_address = models.TextField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name

    class Meta:
        abstract = True

# Resident model inheriting from BaseUser
class Resident(BaseUser):
     # Redefining fields explicitly for clarity (inherited from BaseUser)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=11)
    permanent_address = models.TextField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    USERNAME_FIELD = 'email'  # Setting email as the username field

    class Meta:
        verbose_name = 'Resident'
        verbose_name_plural = 'Residents'

# Appointment model for handling appointment data
class Appointment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=50)
    request = models.TextField(max_length=50,blank=True)
    service_id = models.TextField(max_length=50,blank=True)
    sent_date = models.DateField(auto_now_add=True)
    permanent_address = models.TextField(max_length=100,blank=True)
    accepted = models.TextField(max_length=50,default=False)
    accepted_date = models.DateField(auto_now_add=False, null=True, blank=True)
    appointment_date = models.DateField(auto_now_add=True, null=True, blank=True)
    appointment_time = models.TimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.first_name
    def __str__(self):
        return self.email  # Display the email as the string representation
    
    class Meta:
        ordering = ["-sent_date"] # Order by sent_date in descending order

# Service model for handling different services offered
class Service(models.Model):
    name = models.CharField(max_length=100)
    Description = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='service_images/', null=True, blank=True)

    def __str__(self):
        return self.name  
  
# Custom manager for Resident model, handling user creation
class ResidentManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# Appointment_resident model extending AbstractBaseUser with custom manager
class Appointment_resident(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=11)
    permanent_address = models.TextField()
    email = models.EmailField(unique=True) 
    password = models.CharField(max_length=100)

    objects = ResidentManager()

    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'gender', 'mobile_number', 'permanent_address']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True
    
    class Meta:
        app_label = 'Appointment'

# ConcreteAppointmentResident model for additional user-related fields
class ConcreteAppointmentResident(Appointment_resident):
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='app_users_groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='app_users_permissions'
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='appointment_resident')
    
    class Meta:
        app_label = 'Appointment' # Specify the app label

# FinishedAppointment model for tracking finished appointments
class FinishedAppointment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    request = models.TextField(blank=True)
    service_id = models.TextField(blank=True)
    sent_date = models.DateField(auto_now_add=True)
    rejected_date = models.DateField(auto_now_add=True)
    appointment_date = models.DateField(null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)

# Guardian model for tracking guardian-related information
class Guardian(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    accepted = models.TextField(max_length=50,default=False)
    middle_name= models.CharField(max_length=100)
    request = models.TextField(max_length=100,blank=True)
    permanent_address = models.CharField(max_length=100)
    other_concerns = models.CharField(max_length=254)
    date_of_birth = models.DateField()
    service_id= models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" # Display the full name as the string representation

# Staff model for tracking staff-related information   
class Staff(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='service_images/', null=True, blank=True)

    def __str__(self):
        return self.name
