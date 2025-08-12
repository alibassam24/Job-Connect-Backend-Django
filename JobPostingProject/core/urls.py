from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework import urlpatterns, urls

from .views import *

urlpatterns = [
    # USER-->
    path("register-user/", register_user, name="register-user"),
    path("login-user/", login_user, name="login-user/"),
    path("delete-user/<int:id>/", delete_user, name="delete-user"),
    path("logout-user/", logout_user, name="logout-user"),
    path("update-user/<int:id>/", update_user, name="update-user"),
    # EMPLOYEE-->
    path(
        "create-employee-profile/",
        create_employee_profile,
        name="create-employee-profile",
    ),
    path(
        "view-employee-profile/<int:id>/",
        view_employee_profile,
        name="view-employee-profile",
    ),
    path(
        "edit-employee-profile/<int:id>/",
        edit_employee_profile,
        name="edit-employee-profile",
    ),
    path(
        "create-employer-profile/",
        create_employer_profile,
        name="create-employee-profile",
    ),
    path(
        "edit-employer-profile/<int:id>/",
        edit_employer_profile,
        name="edit-employee-profile",
    ),
    path(
        "view-employer-profile/<int:id>/",
        view_employer_profile,
        name="view-employee-profile",
    ),
    # SKILLS-->
    path(
        "add-skills/",
        add_skills,
        name="add-skills",
    ),
    path(
        "view-skills-by-user-id/<int:id>",
        view_skills_by_user_id,
        name="view-skills-by-user-id",
    ),
    path(
        "remove-skills/<int:id>",
        remove_skills,
        name="remove-skills",
    ),
    # EXPERIENCE-->
    path(
        "add-experience/",
        add_experience,
        name="add-experience",
    ),
    path(
        "get-experiences/",
        get_experiences,
        name="get-experiences",
    ),
    path(
        "get-experience-of-employee/<int:employee_id>/",
        get_experiences_of_employee,
        name="get-experience-of-empoyee",
    ),
    path(
        "remomve-experience/<int:experience_id>/",
        remove_experience,
        name="remove-experience",
    ),
    path(
        "edit-experience/<experience_id>",
        edit_experience,
        name="edit-experience",
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
