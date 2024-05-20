from django import forms
from Appointment.models import Service,Staff

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'Description', 'image']  
        
class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'position', 'image']

class ServicesForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'Description', 'image']