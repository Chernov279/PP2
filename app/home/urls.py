from django.urls import path
from .views import Home, about_us

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about_us', about_us, name='about_us'),
]