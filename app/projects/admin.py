from django.contrib import admin

from projects.models import Project, Column, Task, TaskLog, ProjectUser

# admin.site.register(Project)
# admin.site.register(Column)
# admin.site.register(Task)
# admin.site.register(TaskLog)
# admin.site.register(ProjectUser)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


# @admin.register(ProjectUser)
# class ProjectUserAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("name",)}
#
#
# @admin.register(Column)
# class ColumnAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("name",)}
#
#
# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("name",)}
#
#
# @admin.register(TaskLog)
# class TaskLogAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("name",)}