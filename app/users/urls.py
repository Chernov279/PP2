from django.urls import path
from .views import UserDeleteView, UserCreateView, OtherUserDetailView, UserUpdateView, \
    UserDetailView

urlpatterns = [
    path('', UserDetailView.as_view(), name='user_detail'),
    path('<slug:slug>/', UserDetailView.as_view(), name='user_detail'),
    path('<slug:slug>/create', UserCreateView.as_view(), name='user_create'),
    path('<slug:slug>/edit/', UserUpdateView.as_view(), name='user_update'),
    path('<slug:slug>/delete/', UserDeleteView.as_view(), name='user_delete'),
]