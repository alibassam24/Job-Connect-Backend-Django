from rest_framework import urlpatterns, urls
from rest_framework.urls import path

from .views import *

urlpatterns = [
    path("register-user/", register_user, name="register-user"),
    path("login-user/", login_user, name="login-user/"),
    path("delete-user/<int:id>/", delete_user, name="delete-user"),
]
