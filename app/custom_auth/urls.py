from django.contrib.auth import views as auth_views
from django.urls import path
from .views import SignupView

urlpatterns = [
    # Вход
    path('login/', auth_views.LoginView.as_view(), name='login'),

    # Восстановление пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Регистрация
    path('signup/', SignupView.as_view(), name='signup'),
]