from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Customer, Rating

class UserRegistration(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']
