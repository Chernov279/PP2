from django.urls import path
from .views import home, about_us

urlpatterns = [
    path('', home, name='home'),
    path('about_us', about_us, name='about_us'),
]