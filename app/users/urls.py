from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="user_detail"),
    # path("users/<int:user_id>/", views.index, name="index"),
]