from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm


class UserRegistration(UserCreationForm):

    class Meta:
        model = UserProfile
        fields = ['username', 'password1', 'password2', 'email','image']
