from django.urls import path
from .views import UserDeleteView, UserCreateView, OtherUserDetailView, UserUpdateView, \
    UserDetailView

urlpatterns = [
    path('', UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/create', UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/edit/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]