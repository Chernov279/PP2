from django.urls import path

from .views import ProjectDetailMain

urlpatterns = [
    path('<int:pk>/detail/', ProjectDetailMain.as_view(), name='project_detail_main'),

    # path('<int:pk>/members', ProjectDetailView.as_view(), name='PDM_members'),
    # path('<int:pk>/members/add/', ProjectDetailView.as_view(), name='PDM_members_add'),
    # path('<int:pk>/members/remove/', ProjectDetailView.as_view(), name='PDM_members_remove'),
    # path('<int:pk>/members/change_status/', ProjectDetailView.as_view(), name='PDM_members_change_status'),
    #
    # path('<int:pk>/tasklog', ProjectDetailView.as_view(), name='PDM_tasklog'),
    #
    # path('<int:pk>/task_detail/', ProjectDetailView.as_view(), name='PDM_task_detail'),
    # path('<int:pk>/task/add/', ProjectDetailView.as_view(), name='PDM_task_add'),
    # path('<int:pk>/task/remove/', ProjectDetailView.as_view(), name='PDM_task_remove'),
    # path('<int:pk>/task/update/', ProjectDetailView.as_view(), name='PDM_task_update'),
    #
    # path('<int:pk>/column/add/', ProjectDetailView.as_view(), name='PDM_column_add'),
    # path('<int:pk>/column/remove/', ProjectDetailView.as_view(), name='PDM_column_remove'),
    # path('<int:pk>/column/update/', ProjectDetailView.as_view(), name='PDM_column_update'),

]