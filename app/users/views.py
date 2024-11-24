from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import CustomUser


class UserMeView(LoginRequiredMixin, DetailView):
    # Просмотр своего пользователя GET
    model = CustomUser
    template_name = "users/users_detail.html"
    context_object_name = "user_detail"

    def get_object(self):
        # Возвращаем текущего пользователя
        return self.request.user


class UserCreateView(CreateView):
    model = CustomUser
    template_name = "users/user_form.html"
    fields = ['username', 'email', 'password', 'bio']  # Поля для регистрации
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
    template_name = "users/user_form.html"
    fields = ['username', 'email', 'bio']  # Поля, которые пользователь может редактировать
    success_url = reverse_lazy("user_detail")

    def get_object(self):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user































