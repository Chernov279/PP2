from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify

from .models import CustomUser  # Импорт вашей кастомной модели


class CustomUserCreationForm(UserCreationForm):
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')

        if slug and CustomUser.objects.filter(slug=slug).exists():
            raise forms.ValidationError("Этот слаг уже занят. Пожалуйста, придумайте что-то другое.")

        return slug

    def save(self, commit=True):
        user = super().save(commit=False)

        if not user.slug:
            user.slug = slugify(user.username)

        original_slug = user.slug
        counter = 1
        while CustomUser.objects.filter(slug=user.slug).exists():
            user.slug = f'{original_slug}-{counter}'
            counter += 1

        if commit:
            user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', ]