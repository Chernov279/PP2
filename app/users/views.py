from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import UserUpdateForm
from .models import CustomUser
from projects.views import MyProjectListView
from projects.models import Project


class UserDetailView(LoginRequiredMixin, DetailView):
    # Просмотр своего пользователя GET
    model = CustomUser
    template_name = "users/user_detail.html"
    context_object_name = "user_detail"

    def get_object(self):
        # Возвращаем текущего пользователя
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(created_by=self.request.user)
        return context


class UserCreateView(CreateView):
    model = CustomUser
    template_name = "users/user_form.html"
    fields = ['username', 'email', 'password']  # Поля для регистрации
    success_url = reverse_lazy("login")  # Перенаправление после регистрации

    def form_valid(self, form):
        # Шифрование пароля перед сохранением
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super().form_valid(form)


class OtherUserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/other_user_detail.html"
    context_object_name = "user_profile"

    def get_queryset(self):
        return CustomUser.objects.defer("registration_date")


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = "users/user_update.html"
    fields = ['username', 'email', 'first_name', 'last_name']
    success_url = reverse_lazy('user_detail')

    def get_object(self):
        user = super().get_object()
        if user != self.request.user:
            raise Http404("Вы не можете редактировать чужой профиль.")
        return user

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy('home')  # Перенаправляем на страницу входа после удаления

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            raise Http404("Вы не можете удалить чужой профиль.")
        return obj






























