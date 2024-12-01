from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from users.forms import CustomUserCreationForm


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')  # Переадресация после успешной регистрации

    def form_valid(self, form):
        # Сохраняем пользователя
        user = form.save()
        login(self.request, user)  # Выполняем автоматический вход
        return super().form_valid(form)

    def form_invalid(self, form):
        # Если форма невалидна, то возвращаем страницу с ошибками
        return self.render_to_response(self.get_context_data(form=form))

