from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Project



class ProjectListView(ListView):
    # Просмотр всех проектов GET
    model = Project
    template_name = "projects/project_list.html"  # Шаблон для отображения
    context_object_name = "projects"  # Как будет называться список в шаблоне


class ProjectDetailView(DetailView):
    # Просмотр проекта GET
    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"


class ProjectCreateView(LoginRequiredMixin, CreateView):
    # Создание проектов POST
    model = Project
    fields = ["name", "description"]
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("project_list")  # Перенаправление после создания
    def test_func(self):
        # Только администратор или владелец проекта может редактировать
        project = self.get_object()
        return self.request.user.is_staff or project.created_by == self.request.user


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    # Изменение проектов PUT
    model = Project
    fields = ["name", "description"]
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("project_list")
    def test_func(self):
        # Только администратор или владелец проекта может редактировать
        project = self.get_object()
        return self.request.user.is_staff or project.created_by == self.request.user


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    # Удаление проекта DELETE
    model = Project
    template_name = "projects/project_confirm_delete.html"
    success_url = reverse_lazy("project_list")
    def test_func(self):
        # Только администратор или владелец проекта может редактировать
        project = self.get_object()
        return self.request.user.is_staff or project.created_by == self.request.user

