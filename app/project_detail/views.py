from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Max
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView
import json

from projects.models import Project

from .forms import ColumnForm, TaskForm, ColumnCreateForm, AddProjectUserForm
from .models import Column, Task, TaskLog, ProjectUser
from users.models import CustomUser


class ProjectDetailMain(DetailView):
    model = Project
    template_name = 'project_detail/project_detail_main.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_logs = TaskLog.objects.filter(task__project=self.object).order_by('-created_at')
        context['columns'] = Column.objects.filter(project=self.object).order_by('position')
        context['task_logs'] = task_logs
        context['project_users'] = ProjectUser.objects.filter(project=self.object)
        return context


class ColumnCreateView(View):
    def get(self, request, pk):
        """
        Отображение формы создания колонки для проекта с указанным pk.
        """
        form = ColumnCreateForm()
        project = get_object_or_404(Project, pk=pk)
        return render(request, 'project_detail/column_create.html', {'form': form, 'project': project})

    def post(self, request, pk):
        """
        Обработка данных формы создания колонки для проекта с указанным pk.
        """
        form = ColumnCreateForm(request.POST)
        if form.is_valid():
            # Получаем данные из формы
            name = form.cleaned_data['name']
            color = form.cleaned_data['color']
            tasks = request.POST.getlist('tasks[]')

            # Проверяем, существует ли проект с указанным pk
            project = get_object_or_404(Project, pk=pk)

            # Нахождение максимального значения позиции среди колонок проекта
            max_position = Column.objects.filter(project=project).aggregate(Max('position'))['position__max'] or 0

            # Создание новой колонки
            column = Column.objects.create(
                name=name,
                color=color,
                project=project,
                position=max_position + 1,  # Увеличиваем позицию на 1
            )

            # Добавление задач в созданную колонку
            for task_name in tasks:
                if task_name.strip():  # Если название задачи не пустое
                    Task.objects.create(
                        column=column,
                        project=project,
                        title=task_name.strip(),
                    )

            # Перенаправление на главную страницу проекта
            return redirect('project_detail_main', pk=project.pk)

        # Если форма не прошла валидацию, возвращаем ее с ошибками
        project = get_object_or_404(Project, pk=pk)
        return render(request, 'project_detail/column_create.html', {'form': form, 'project': project})


class AddColumnView(View):
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = ColumnForm(request.POST)
        if form.is_valid():
            column = form.save(commit=False)
            column.project = project
            column.save()
            return redirect('project_detail_main', pk=pk)
        return redirect('project_detail_main', pk)


class UpdateColumnView(View):
    def get(self, request, pk, column_id):
        column = get_object_or_404(Column, id=column_id, project_id=pk)
        project = column.project
        return render(request, 'project_detail/column_update.html', {'column': column, 'project': project})

    def post(self, request, pk, column_id):
        column = get_object_or_404(Column, id=column_id, project_id=pk)

        # Обновление названия и цвета колонки
        column.name = request.POST.get('name')
        column.color = request.POST.get('color')
        column.save()

        for key, value in request.POST.items():
            if key.startswith('tasks[') and 'new' not in key:
                task_id = key[6:-1]  # Извлекаем ID задачи
                task = Task.objects.get(id=task_id, column=column)
                task.title = value  # Название задачи
                task.description = request.POST.get(f'tasks_description[{task_id}]', task.description)  # Описание задачи
                task.save()

                # Логируем изменение задачи
                TaskLog.objects.create(
                    task=task,
                    message=f"Задача '{task.title}' была обновлена в колонке '{task.column.name}'"
                )

        # Добавление новых задач
        new_tasks = request.POST.getlist('tasks[new][]', [])
        new_descriptions = request.POST.getlist('tasks_description[new][]', [])

        for title, description in zip(new_tasks, new_descriptions):
            if title.strip():
                new_task = Task.objects.create(
                    title=title,
                    description=description,
                    column=column,
                    project_id=pk
                )

                # Логируем добавление новой задачи
                TaskLog.objects.create(
                    task=new_task,
                    message=f"Новая задача'{new_task.title}' была создана в колонке '{new_task.column.name}'"
                )
        return redirect('project_detail_main', pk)  # Замените на ваш URL для возврата


class RemoveColumnView(View):
    def post(self, request, pk, column_id):
        column = get_object_or_404(Column, id=column_id, project_id=pk)
        column.delete()
        return redirect('project_detail_main', pk=pk)


class AddTaskView(View):
    def post(self, request, pk, column_id):
        # Проверяем, что колонка принадлежит проекту
        column = get_object_or_404(Column, id=column_id, project_id=pk)

        # Получаем данные из запроса
        data = json.loads(request.body)
        task_title = data.get('title')

        if not task_title:
            return JsonResponse({'error': 'Название задачи не может быть пустым'}, status=400)

        # Создаем задачу
        task = Task.objects.create(
            column=column,
            project_id=pk,
            title=task_title
        )

        # Возвращаем данные о новой задаче
        return JsonResponse({'id': task.id, 'title': task.title}, status=201)


class UpdateTaskView(View):
    def post(self, request, pk, task_id):
        task = get_object_or_404(Task, id=task_id, column__project_id=pk)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project_detail_main', pk=pk)
        return JsonResponse({'error': 'Invalid data'}, status=400)


class RemoveTaskView(View):
    def post(self, request, pk, task_id):
        task = get_object_or_404(Task, id=task_id, column__project_id=pk)
        print(f"Удаляем задачу с ID {task.id}")
        task.delete()
        return JsonResponse({'id': task.id, 'title': task.title}, status=201)


class MoveTaskView(View):
    def post(self, request, pk):
        task_id = request.POST.get('task_id')
        target_column_id = request.POST.get('target_column_id')
        task = get_object_or_404(Task, id=task_id, column__project_id=pk)
        target_column = get_object_or_404(Column, id=target_column_id, project_id=pk)
        task.column = target_column
        task.save()
        return JsonResponse({'status': 'success'})


class TaskLogListView(View):
    def get(self, request, pk):
        # Получаем проект
        project = get_object_or_404(Project, id=pk)

        # Получаем связанные таск-логи, сортируем по времени
        task_logs = TaskLog.objects.filter(task__project=project).order_by('-created_at')

        # Формируем JSON-ответ
        logs_data = [
            {
                'timestamp': log.created_at.strftime('%d.%m.%Y %H:%M'),
                'description': log.message,
            }
            for log in task_logs
        ]

        return JsonResponse({'task_logs': logs_data})


class AddProjectUserView(LoginRequiredMixin, View):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = AddProjectUserForm()
        return render(request, 'project_detail/add_project_user.html', {'form': form, 'project': project})

    def post(self, request, pk):
        form = AddProjectUserForm(request.POST)
        if form.is_valid():
            try:
                user = form.cleaned_data['user']
                project = get_object_or_404(Project, pk=pk)
                # Добавляем пользователя в проект
                ProjectUser.objects.create(project=project, user=user, status="member")
            except Exception as e:
                return render(request, 'project_detail/add_project_user.html', {'form': form, 'project': project})
        return HttpResponseRedirect(reverse('project_detail_main', args=[pk]))





class RemoveUserFromProjectView(View):
    def post(self, request, project_id, user_id):
        # Получаем проект и пользователя для удаления
        project = get_object_or_404(Project, id=project_id)
        user_to_remove = get_object_or_404(ProjectUser, project=project, user_id=user_id)

        # Проверяем, что пользователь имеет права для удаления
        if user_to_remove.status != 'creator' and request.user != project.created_by and not request.user.is_staff:
            raise Http404("У вас нет прав для удаления этого пользователя.")

        # Удаляем пользователя из проекта
        user_to_remove.delete()
        return redirect('project_detail_main', pk=project.id)


class LeaveProjectView(View):
    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        project_user = get_object_or_404(ProjectUser, project=project, user=request.user)

        # Проверяем, что пользователь не является создателем проекта
        if project_user.status == 'creator':
            raise Http404("Создатель проекта не может покинуть проект.")

        project_user.delete()  # Удаляем пользователя из проекта
        return redirect('project_list_my')