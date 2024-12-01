from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Импорт вашей кастомной модели


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', ]