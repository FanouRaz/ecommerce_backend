from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("users/",views.getUsers, name="get users")
]
