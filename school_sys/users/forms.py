from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'role', 'nombre')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
