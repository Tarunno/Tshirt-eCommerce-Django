from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Custom

class UserRegistration(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']

class CustomTshirtForm(forms.ModelForm):
    class Meta:
        model = Custom
        fields = ['customer', 'order', 'design', 'color', 'tshirt_size', 'design_size', 'quentity']
