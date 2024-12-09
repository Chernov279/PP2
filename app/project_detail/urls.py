from django.urls import path

from .views import (
    ProjectDetailMain,
    AddColumnView,
    UpdateColumnView,
    RemoveColumnView,
    AddTaskView,
    UpdateTaskView,
    RemoveTaskView,
    MoveTaskView,
    ColumnCreateView
)

urlpatterns = [
    path('<int:pk>/detail/', ProjectDetailMain.as_view(), name='project_detail_main'),

    # path('<int:pk>/members', ProjectDetailView.as_view(), name='PDM_members'),
    # path('<int:pk>/members/add/', ProjectDetailView.as_view(), name='PDM_members_add'),
    # path('<int:pk>/members/remove/', ProjectDetailView.as_view(), name='PDM_members_remove'),
    # path('<int:pk>/members/change_status/', ProjectDetailView.as_view(), name='PDM_members_change_status'),

    path('<int:pk>/column/add/', ColumnCreateView.as_view(), name='PDM_column_add'),
    path('<int:pk>/column/update/<int:column_id>/', UpdateColumnView.as_view(), name='PDM_column_update'),
    path('<int:pk>/column/remove/<int:column_id>/', RemoveColumnView.as_view(), name='PDM_column_remove'),

    # Задачи
    path('<int:pk>/task/add/<int:column_id>/', AddTaskView.as_view(), name='PDM_task_add'),
    path('<int:pk>/task/update/<int:task_id>/', UpdateTaskView.as_view(), name='PDM_task_update'),
    path('<int:pk>/task/remove/<int:task_id>/', RemoveTaskView.as_view(), name='PDM_task_remove'),
    path('<int:pk>/task/move/', MoveTaskView.as_view(), name='PDM_task_move'),
]