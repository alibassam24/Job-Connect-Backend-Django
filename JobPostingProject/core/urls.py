from rest_framework import urlpatterns, urls
from rest_framework.urls import path

from .views import *

urlpatterns = [
    #USER-->
    path("register-user/", register_user, name="register-user"),
    path("login-user/", login_user, name="login-user/"),
    path("delete-user/<int:id>/", delete_user, name="delete-user"),
    #EMPLOYEE-->
    path("create-employee-profile",create_employee_profile,name="create-employee-profile"),

]
