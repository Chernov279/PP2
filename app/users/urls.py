from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("", views.index, name="index"),
    # path("users/<int:user_id>/", views.index, name="index"),

]