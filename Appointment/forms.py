from django import forms
from .models import Resident

# ResidentForm is a ModelForm that creates a form based on the Resident model
class ResidentForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Resident
        fields = '__all__'

# LoginForm is a regular form (not a ModelForm) for handling user login
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

