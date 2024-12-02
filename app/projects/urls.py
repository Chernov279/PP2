from django.urls import path
from .views import (
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView, MyProjectListView,
)

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('my/', MyProjectListView.as_view(), name='project_list_my'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('<slug:slug>/edit/', ProjectUpdateView.as_view(), name='project_update'),
    path('<slug:slug>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
]