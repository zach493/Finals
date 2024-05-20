from django.contrib.auth import logout,authenticate, login
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.http import JsonResponse
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage, message
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth.views import LogoutView
from django.views import View
from django.contrib import messages
from Appointment.models import Appointment, Service ,ConcreteAppointmentResident,Guardian ,Appointment_resident, Staff
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView,TemplateView
import datetime
from django.template.loader import render_to_string, get_template

# User login view
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('dashboard')  # Redirect to admin panel for superusers
            else:
                return redirect('home')  # Redirect to the home page for residents
        else:
            error = "Invalid email or password"
            return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')

# User registration view
def register_view(request):
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']
        date_of_birth = request.POST['date_of_birth']
        age = request.POST['age']
        gender = request.POST['gender']
        mobile_number = request.POST['mobile_number']
        permanent_address = request.POST['permanent_address']
        email = request.POST['email']
        password = request.POST['password']

        try:
            if User.objects.filter(email=email).exists():
                raise IntegrityError("A user with this email already exists.")
            user = User.objects.create_user(username=email,email=email, password=password,
                                             first_name=first_name, last_name=last_name)

           
            resident = ConcreteAppointmentResident.objects.create(user=user, first_name=first_name,
                                                                  middle_name=middle_name,
                                                                  last_name=last_name, date_of_birth=date_of_birth,
                                                                  age=age,email=email, gender=gender,
                                                                  mobile_number=mobile_number,
                                                                  permanent_address=permanent_address)

            # Redirect to a success page or login page
            return redirect('login.html')
        except IntegrityError as e:
            # Handle the integrity error (email already exists)
            error = "Email already exists. Please use a different email."
            return render(request, 'register.html', {'error': error})

    else:
        return render(request, 'register.html')

# Home page view with context data
class HomeTemplateView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staffs'] = Staff.objects.all()
        context['services'] = Service.objects.all()
        return context

# View to refresh session
def refresh_session(request):
    request.session.modified = True  # Update session modified time
    return JsonResponse({'status': 'Session refreshed'})

# View for successful appointment
class Successful_AppointmentView(TemplateView):
    template_name = 'successful_appointment.html'

# Appointment view with login required
class Error_AppointmentView(TemplateView):
    template_name = 'error_appointment.html'

@method_decorator(login_required, name='dispatch')
class AppoiTemplateView(TemplateView):
    template_name = "appointment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        role = request.POST.get("role")

        if role == "patient":
            return self.handle_patient_form(request, role)  
        elif role == "guardian":
            return self.handle_guardian_form(request, role)  
        else:
        # Handle invalid role option, maybe redirect back to the form page with an error message
            return HttpResponseBadRequest("Invalid role option")
        
    # Function to handle appointment form submissions for patients
    def handle_patient_form(self, request, role):
        # Get the currently logged-in user
        user = request.user
        # Retrieve the resident details based on the user's email
        resident = Appointment_resident.objects.get(email=user.email)  
        first_name = resident.first_name
        age = resident.age
        last_name = resident.last_name
        phone = resident.mobile_number
        permanent_address = resident.permanent_address
        accepted = "Waiting"
        accepted_date = timezone.now()

        # Retrieve appointment details from the form submission
        appointment_time = request.POST.get("appointment_time")
        appointment_date = request.POST.get("appointment_date")
        service_id = request.POST.get("service_id")
        request_type = "Patient"  

        try:
            # Create a new appointment object in the database
            appointment = Appointment.objects.create(
                first_name=first_name,
                last_name=last_name,
                age=age,
                phone=phone,
                permanent_address=permanent_address,
                accepted=accepted,
                accepted_date=accepted_date,
                email=user.email, 
                appointment_time=appointment_time,
                appointment_date=appointment_date,
                service_id=service_id,
                request=request_type  
        )
            # Store appointment details in the session for future reference
            request.session['appointment'] = {
                'first_name': first_name,
                'last_name': last_name,
                'age': age,
                'phone': phone,
                'permanent_address': permanent_address,
                'appointment_time': appointment_time,
                'appointment_date': appointment_date,
                'service_id': service_id,
                'request': request_type,  
        }
            return redirect("success_page")
        except IntegrityError:
            # Redirect to the error page if an IntegrityError occurs
            return redirect("error_page")

# Function to handle appointment form submissions for guardians
def handle_guardian_form(self, request, role):
    # Retrieve guardian details from the form submission
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    middle_name = request.POST.get("middle_name")
    accepted = "Waiting"
    date_of_birth = request.POST.get("date_of_birth")
    service_id = request.POST.get("service_id")
    permanent_address = request.POST.get("permanent_address")
    other_concerns = request.POST.get("other_concerns")
    age = request.POST.get("age")
    request_type = "Guardian" 

    try:
        guardian = Guardian.objects.create(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            accepted=accepted,
            date_of_birth=date_of_birth,
            service_id=service_id,
            permanent_address=permanent_address,
            other_concerns=other_concerns,
            age=age,
            request=request_type 
        )
         # Store guardian details in the session for future reference
        request.session['guardian'] = {
            'first_name': first_name,
            'last_name': last_name,
            'middle_name': middle_name,
            'date_of_birth': date_of_birth,
            'age': age,
            'permanent_address': permanent_address,
            'service_id': service_id,
            'other_concerns': other_concerns,
            'request': request_type,  
        }
         # Redirect to the success page upon successful guardian creation
        return redirect("success_page")
    except IntegrityError:
         # Redirect to the error page if an IntegrityError occurs
        return redirect("error_page")

# User logout view
@login_required(login_url='login/')
def logout_user(request):
    logout(request)
    return redirect('home')

#  View to display user inbox with their appointments
@login_required
def user_inbox(request):
    user_email = request.user.email
    appointments = Appointment.objects.filter(email=user_email)
    
    return render(request, 'residents_inbox.html', {'appointments': appointments})






