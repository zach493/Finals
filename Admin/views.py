#Django modules and functions
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse,JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from Appointment.models import Appointment, Service, Staff, Appointment_resident,FinishedAppointment, Guardian
from django.db import IntegrityError
import datetime
from .forms import StaffForm,ServicesForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

#Function to check if the user is a superuser
def is_superuser(user):
    return user.is_superuser

#DASHBOARD, accessible only to logged-in superusers
class DashboardTemplateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = 'login' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Gather and add various counts to the context
        total_residents = Appointment_resident.objects.count()
        context['total_residents'] = total_residents
        total_appointments = Appointment.objects.count()
        context['total_appointments'] = total_appointments
        total_services = Service.objects.count()
        context['total_services'] = total_services
        total_staff = Staff.objects.count()
        context['total_staff'] = total_staff
        return context

    def test_func(self):
        return self.request.user.is_superuser

# Admin base view
class SATemplateView(TemplateView):
    template_name = 'adminbase.html'

# Managing staff, accessible only to logged-in superusers
class StaffTemplateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'staff.html'
    login_url = 'login' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add all staff members to the context
        context['staffs'] = Staff.objects.all()
        return context
    
    def test_func(self):
        return self.request.user.is_superuser
    
# Function to delete a staff member
def delete_staff(request, staff_id):
    staff_member = get_object_or_404(Staff, id=staff_id)
    
    if request.method == 'POST':
        staff_member.delete()
        return redirect('staff')  

# Function to edit a staff member's details
def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)

    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('staff')
    else:
        form = StaffForm(instance=staff)

    return render(request, 'edit_staff.html', {'form': form})

# Managing services, accessible only to logged-in superusers
class ServicesTemplateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'services.html'
    login_url = 'login' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
         # Add all services to the context
        context['services'] = Service.objects.all()
        return context
    
    def test_func(self):
        return self.request.user.is_superuser

# Delete a service, only accessible via POST request by superusers
@require_POST
@login_required
@user_passes_test(is_superuser)
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    return redirect('services')

# Function to check if the user is a superuser
def is_superuser(user):
    return user.is_superuser

# DASHBOARD, accessible only to logged-in superusers (duplicate)
class DashboardTemplateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_residents'] = Appointment_resident.objects.count()
        context['total_appointments'] = Appointment.objects.count()
        context['total_services'] = Service.objects.count()
        context['total_staff'] = Staff.objects.count()
        return context

    def test_func(self):
        return self.request.user.is_superuser

class SATemplateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'adminbase.html'
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_superuser

# View for managing staff
class StaffTemplateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'staff.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add all staff members to the context
        context['staffs'] = Staff.objects.all()
        return context

    def test_func(self):
        return self.request.user.is_superuser

# Function to delete staff
@require_POST
@login_required
@user_passes_test(is_superuser)
def delete_staff(request, staff_id):
    staff_member = get_object_or_404(Staff, id=staff_id)
    staff_member.delete()
    return redirect('staff')

# Function to edit/update staff
@login_required
@user_passes_test(is_superuser)
def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)

    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('staff')
    else:
        form = StaffForm(instance=staff)

    return render(request, 'edit_staff.html', {'form': form})

# View for managing services
class ServicesTemplateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'services.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add all services to the context
        context['staffs'] = Service.objects.all()
        return context

    def test_func(self):
        return self.request.user.is_superuser

# Function to delete services
@require_POST
@login_required
@user_passes_test(is_superuser)
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    return redirect('services')

# Function to edit services
@login_required
@user_passes_test(is_superuser)
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        form = ServicesForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('services')
    else:
        form = ServicesForm(instance=service)

    return render(request, 'edit_service.html', {'form': form})

# View for managing residents
class ResidentsTemplateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'residents.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
         # Add all residents to the context
        context['data'] = Appointment_resident.objects.all()
        return context

    def test_func(self):
        return self.request.user.is_superuser

# Function to delete resident
@login_required
@user_passes_test(is_superuser)
def delete_resident(request, resident_id):
    resident_who = get_object_or_404(Appointment_resident, id=resident_id)
    resident_who.delete()
    return redirect('residents')

# View for managing appointments
class AppointmentTemplateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'adm_appointment.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add all appointments to the context
        context['appointments'] = Appointment.objects.all()
        return context

    def test_func(self):
        return self.request.user.is_superuser

# General function to update the status of an appointment
def update_status(request, model_class, status, appointment_type):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        appointment = model_class.objects.get(id=appointment_id)
        appointment.accepted = status
        appointment.save()
    return redirect(reverse('adm_app') + f'?appointment_type={appointment_type}')

# Function to accept an appointment
@login_required
@user_passes_test(is_superuser)
def accept_appointment(request):
    return update_status(request, Appointment, "Accepted", 'patient')

# Function to reject an appointment
@login_required
@user_passes_test(is_superuser)
def reject_appointment(request):
    return update_status(request, Appointment, "Rejected", 'patient')

# Function to move an appointment to finished
@login_required
@user_passes_test(is_superuser)
def move_to_finished(request):
    return update_status(request, Appointment, "Finished", 'patient')

# View for managing guardian appointments
class GuardianTemplateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'guardian_appointment.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
         # Add all guardian appointments to the context
        context['guardian_appointments'] = Guardian.objects.all()
        return context

    def test_func(self):
        return self.request.user.is_superuser

# Function to reject a guardian appointment
@login_required
@user_passes_test(is_superuser)
def accept_appointment_guardian(request):
    return update_status(request, Guardian, "Accepted", 'guardian')

# Function to move a guardian appointment to finished
@login_required
@user_passes_test(is_superuser)
def reject_appointment_guardian(request):
    return update_status(request, Guardian, "Rejected", 'guardian')

# View for viewing the history of finished appointments
@login_required
@user_passes_test(is_superuser)
def move_to_finished_guardian(request):
    return update_status(request, Guardian, "Finished", 'guardian')

class HistoryTemplateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'history.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        # Add all finished appointments to the context
        context = super().get_context_data(**kwargs)
        context['appointments'] = FinishedAppointment.objects.all()
        return context

    def test_func(self):
        return self.request.user.is_superuser

# View for some custom report (CR)
class CrTemplateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'cr.html'
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_superuser

# Function to add a new service
@login_required
@user_passes_test(is_superuser)
def add_service(request):
    if request.method == 'POST':
        name = request.POST.get('name')  
        description = request.POST.get('Description') 
        image = request.FILES.get('image')  

        try:
            if Service.objects.filter(name=name).exists():
                raise IntegrityError("A Service with this name already exists.")
            service = Service.objects.create(name=name, Description=description, image=image)

            # Redirect to a page showing all services or a success page
            return redirect('services') 

        except IntegrityError as e:
            error = "Service already exists. Please add another service."
            return render(request, 'services.html', {'error': error})

    else:
        return render(request, 'services.html')

 # Function to add a new staff member   
@login_required
@user_passes_test(is_superuser)
def add_staff(request):
    if request.method == 'POST':
        name = request.POST.get('newName')
        position = request.POST.get('newPosition')
        image = request.FILES.get('officialImage')

        try:
            if Staff.objects.filter(name=name).exists():
                raise IntegrityError("A staff member with this name already exists.")
            staff_member = Staff.objects.create(name=name, position=position, image=image)

            # Redirect to a page showing all staff members or a success page
            return redirect('staff') 

        except IntegrityError as e:
            error = "A staff member with this name already exists. Please add another staff member."
            return render(request, 'staff.html', {'error': error})

    else:
        return render(request, 'staff.html')
    
# Function to log out a user
@login_required
def logout_view(request):
    logout(request)
    return redirect('login.html')