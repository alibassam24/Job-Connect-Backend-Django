from rest_framework import urlpatterns, urls
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    #USER-->
    path("register-user/", register_user, name="register-user"),
    path("login-user/", login_user, name="login-user/"),
    path("delete-user/<int:id>/", delete_user, name="delete-user"),
    path("logout-user/", logout_user, name="logout-user"),
    path("update-user/<int:id>",update_user,name="update-user"),
    #EMPLOYEE-->
    path("create-employee-profile/",create_employee_profile,name="create-employee-profile"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)