from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("users/",views.getUsers, name="get users"),
    path("user/<int:id>",views.getUserById, name="get user by id"),
    path("deleteUser/<int:id>",views.deleteUserById,name="delete user"),
    path("updateUser/<int:id>",views.updateUser,name="update user"),
    path("createUser/",views.createUser,name="create user")
]
