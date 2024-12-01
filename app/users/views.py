from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import UserUpdateForm
from .models import CustomUser


class UserDetailView(LoginRequiredMixin, DetailView):
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
        print(form.cleaned_data)
        return redirect(self.success_url)


# class UserUpdateView(LoginRequiredMixin, UpdateView):
#     model = CustomUser
#     template_name = "users/user_update.html"
#     fields = ['username', 'email', 'first_name', 'last_name']  # Поля для редактирования
#     success_url = reverse_lazy('user_detail')  # Убедитесь, что success_url верен
#
#     def get_object(self):
#         user = super().get_object()
#
#         # Проверяем, что текущий пользователь - владелец
#         if user != self.request.user:
#             raise Http404("Вы не можете редактировать чужой профиль.")
#         return user


# class UpdateProfileView(UpdateView):
#     def get(self, request, pk):
#         user = get_object_or_404(CustomUser, pk=pk)
#         form = UserUpdateForm(instance=user)
#         return render(request, 'users/user_update.html', {'form': form, 'user': user})
#
#     def post(self, request, pk):
#         user = get_object_or_404(CustomUser, pk=pk)
#         form = UserUpdateForm(request.POST, instance=user)
#         if form.is_valid():
#             print(form.cleaned_data)  # Выводим очищенные данные для отладки
#             form.save()
#             return redirect('user_detail', pk=user.pk)
#         return render(request, 'users/users_detail.html', {'form': form, 'user': user})


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user
































