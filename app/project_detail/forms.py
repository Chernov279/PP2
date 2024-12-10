from django import forms
from .models import Project, Column, Task, TaskLog
from users.models import CustomUser


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название проекта'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание проекта'}),
        }


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ['name', 'position', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название колонки'}),
            'position': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Позиция'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
        }


class ColumnCreateForm(forms.Form):
    name = forms.CharField(max_length=255, label="Название колонки")
    color = forms.CharField(max_length=7, label="Цвет колонки")
    tasks = forms.CharField(widget=forms.Textarea, required=False, label="Список задач (разделяйте новой строкой)")


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название задачи'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание'}),
            'status': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('todo', 'To Do'),
                ('in_progress', 'In Progress'),
                ('review', 'Review'),
                ('done', 'Done')
            ]),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }


class TaskLogForm(forms.ModelForm):
    class Meta:
        model = TaskLog
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Сообщение лога'}),
        }


class AddProjectUserForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        to_field_name="id",  # Чтобы использовать id для сохранения
        empty_label="Выберите пользователя",
        label="Пользователь",
        widget=forms.Select(attrs={'class': 'form-control'})
    )