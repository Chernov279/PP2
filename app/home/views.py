from django.shortcuts import render
from django.views.generic import ListView

from projects.models import Project


class Home(ListView):
    model = Project
    template_name = 'home/home_page.html'  # Шаблон, где будет отображаться список
    context_object_name = 'projects'


def about_us(request):
    return render(request, "home/about_us.html")
