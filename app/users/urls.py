from django.urls import path
from .views import UserMeView, UserDeleteView, UserCreateView, OtherUserDetailView, UserUpdateView

urlpatterns = [
    path('', UserMeView.as_view(), name='user_detail'),
    path('create/', OtherUserDetailView.as_view(), name='user_create'),
    path('<int:pk>/', UserCreateView.as_view(), name='user_other_get'),
    path('<int:pk>/edit/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]