from django.db import models

from users.models import CustomUser


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='project_creator'
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table: str = "project"
        verbose_name: str = "Проект"
        verbose_name_plural: str = "Проекты"


class Column(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='columns')
    name = models.CharField(max_length=255)
    position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)


class TaskLog(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='logs')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ProjectUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_users')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_projects')
    status = models.CharField(max_length=15, default="member")

    class Meta:
        unique_together = ('project', 'user')
