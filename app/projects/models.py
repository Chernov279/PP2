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
