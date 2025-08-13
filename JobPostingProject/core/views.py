from datetime import datetime

from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (api_view, authentication_classes,
                                       parser_classes, permission_classes)
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *

# -------------------------------USER----------------------------------------->>>>


@api_view(["POST"])
def register_user(request):
    email = request.data["username"]
    password = request.data["password"]

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():

        user = serializer.save()
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)

        return Response(
            {
                "status": "success",
                "message": "user created successfully",
                "Data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    else:
        return Response(
            {"status": "failed", "message": "Invalid data", "Error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
def login_user(request):

    username = request.data["username"]
    # username = request.data.get("username", "")
    password = request.data["password"]

    user = authenticate(username=username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"status": "success", "message": "login successful", "Token": token.key},
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"status": "failed", "message": "Invalid data"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request, id):
    if not id:
        return Response({"status": "failed", "message": "user not found"})
    else:
        try:
            user = User.objects.get(id=id)
            if request.user.id == user.id:
                user.delete()
                return Response(
                    {"status": "success", "message": "user deleted successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"status": "failed", "message": "not allowed"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except User.DoesNotExist:
            return Response(
                {"status": "failed", "message": "User not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# EDIT USER
@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request, id):
    if request.user.id == id:
        try:
            user = User.objects.get(id=id)
            serializer = UpdateUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(
                    {
                        "status": "failed",
                        "message": "invalid data",
                        "error": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except User.DoesNotExist:
            return Response(
                {"status": "failed", "message": "user not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {"status": "failed", "message": "permission denied"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        request.user.auth_token.delete()
        return Response(
            {"status": "success", "message": "token deleted successfully"},
            status=status.HTTP_200_OK,
        )
    except:
        return Response(
            {"Status": "failed", "Message": "exception was thrown"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# -------------------------------EmployeeProfile----------------------------------------->>>>


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_employee_profile(request):
    data = request.data.copy()
    data["user"] = request.user.id
    serializer = EmployeeProfileSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "status": "success",
                "message": "employee created",
                "Data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
    else:
        return Response(
            {
                "status": "failed",
                "message": "invalid data",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_employee_profile(request, id):
    try:
        employee = EmployeeProfile.objects.get(id=id)
        if request.user.id == employee.user.id:
            serializer = EmployeeProfileSerializer(employee)
            return Response(
                {
                    "status": "success",
                    "message": "employee fetched",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": "failed", "message": "not authorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    except EmployeeProfile.DoesNotExist:
        return Response(
            {"status": "failed", "message": "Employee Not found"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_employee_profile(request, id):
    if request.user.id == id:
        try:
            employee = EmployeeProfile.objects.get(id=id)
            serializer = UpdateEmployeeSerializer(
                employee, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": "success",
                        "message": "employee profile updated successfully",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "status": "failed",
                        "message": "invalid data",
                        "Errors": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except EmployeeProfile.DoesNotExist:
            return Response(
                {"status": "failed", "message": "Employee not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
    else:
        return Response(
            {"status": "failed", "message": "unauthorized"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


# -------------------------------EmployeerProfile----------------------------------------->>>>


@api_view(["POST"])
def create_employer_profile(request):
    data = request.data.copy()
    data["user"] = request.user.id
    serializer = EmployerProfileSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "status": "success",
                "message": "employer created",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
    else:
        return Response(
            {
                "status": "failed",
                "message": "invalid data",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
def view_employer_profile(request, id):
    if not id:
        return Response(
            {"status": "failed", "message": "id not found"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    else:
        try:
            employer = EmployerProfile.objects.get(id == id)
            serializer = EmployeeProfileSerializer(employer)
            # if serializer.is_valid():
            return Response(
                {
                    "status": "success",
                    "message": "Employee fetched successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
            # else:
            #   return Response({"":"","":"","":serializer.errors},status=status.)
        except EmployeeProfile.DoesNotExist:
            return Response(
                {"status": "failed", "message": "employer not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(["PATCH"])
def edit_employer_profile(request, id):
    try:
        employer = EmployerProfile.objects.get(id=id)
        serializer = UpdateEmployerSerializer(employer, data=request.data, partial=True)
        if serializer.is_valid():
            return Response(
                {
                    "status": "success",
                    "message": "emploer profile updated",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return
    except EmployerProfile.DoesNotExist:
        return Response(
            {
                "status": "failed",
                "message": "employer not found",
            },
            status=status.HTTP_404_NOT_FOUND,
        )


# -------------------------------Skills----------------------------------------->>>>
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_skills(request):
    data = request.data.copy()
    id = request.user.id
    try:
        employee = EmployeeProfile.objects.get(user=id)
        # data["employee"] = employee.GET.get("id","") GET only works on request
        data["employee"] = employee.id
        serializer = SkillsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "skill added",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "status": "failed",
                    "message": "invalid data",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    except EmployeeProfile.DoesNotExist:
        return Response(
            {
                "status": "failed",
                "message": "employee not found",
            },
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_skills_by_user_id(request, id):
    skills = Skills.objects.filter(employee=id)
    serializer = SkillsSerializer(skills, many=True)
    return Response(
        {
            "status": "success",
            "messaage": "skills fetched successfully",
            "data": serializer.data,
        },
        status=status.HTTP_202_ACCEPTED,
    )


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_skills(request, id):
    try:
        skill = Skills.objects.get(id=id)
        employee = EmployeeProfile.objects.get(user=request.user)

        if employee in skill.employee.all():
            skill.delete()
            return Response(
                {"status": "success", "message": "skill deleted successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": "failed", "message": "user not allowed"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    except Skills.DoesNotExist:
        return Response(
            {"status": "failed", "message": "skill not found"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# -------------------------------Experience----------------------------------------->>>>


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_experience(request):
    data = request.data.copy()
    try:
        user_id = request.user.id
        try:
            employee = EmployeeProfile.objects.get(user=user_id)
        except EmployeeProfile.DoesNotExist:
            return Response(
                {"status": "failed", "message": "no employee found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data["employee"] = employee.id
        start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
    except ValueError:
        return Response(
            {"status": "failed", "message": "invalid date format"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    data["duration"] = (end_date - start_date).days
    serializer = ExperienceSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "status": "success",
                "message": "experience added successfully",
            },
            status=status.HTTP_201_CREATED,
        )
    else:
        return Response(
            {
                "status": "failed",
                "message": "invalid data",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_experiences(request):

    user_id = request.user.id
    try:
        employee = EmployeeProfile.objects.get(user=user_id)
    except EmployeeProfile.DoesNotExist:
        return Response(
            {
                "status": "failed",
                "message": "employee not found",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    experiences = Experience.objects.filter(employee=employee)
    serializer = ExperienceSerializer(experiences, many=True)
    return Response(
        {
            "status": "success",
            "message": "experiences found",
            "data": serializer.data,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_experiences_of_employee(request, employee_id):
    try:
        employee = EmployeeProfile.objects.get(id=employee_id)
    except EmployeeProfile.DoesNotExist:
        return Response(
            {"Status": "failed", "message": "employee not found"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    experiences = Experience.objects.filter(employee=employee)
    if Experience.objects.filter(employee=employee).values().exists():
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(
            {
                "status": "success",
                "message": "experiences fetched",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {
                "status": "success",
                "message": "no experience found",
            },
            status=status.HTTP_200_OK,
        )


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_experience(request, experience_id):
    user_id = request.user.id
    try:
        employee = EmployeeProfile.objects.get(user=user_id)
    except:
        return Response(
            {"status": "failed", "message": "employee not found against user id"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    employee_id = employee.id

    try:
        experience = Experience.objects.get(id=experience_id)
        if employee_id == experience.employee.id:
            experience.delete()
            return Response(
                {"status": "success", "message": "experience deleted successfully"},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(
                {"status": "failed", "message": "unauthorized"},
                status=status.HTTP_403_FORBIDDEN,
            )
    except Experience.DoesNotExist:
        return Response(
            {"status": "failed", "message": "experience not found"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_experience(request, experience_id):
    try:
        experience = Experience.objects.get(id=experience_id)
    except Experience.DoesNotExist:
        return Response(
            {
                "status": "failed",
                "message": "experience not found",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    seriazlizer = ExperienceSerializer(experience, data=request.data, partial=True)
    if seriazlizer.is_valid():
        seriazlizer.save()
        return Response(
            {"status": "success", "message": "updated experience successfully"},
            status=status.HTTP_201_CREATED,
        )
    else:
        return Response(
            {
                "status": "failed",
                "message": "invalid data",
                "errors": seriazlizer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# -------------------------------Job----------------------------------------->>>


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_job(request):
    data = request.data.copy()
    user_id = request.user.id
    try:
        employer = EmployerProfile.objects.get(user=user_id)
    except EmployeeProfile.DoesNotExist:
        return Response(
            {
                "status": "failed",
                "message": "Employer not found",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    data["employer"] = employer.id
    serializer = JobSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"status": "success", "message": "job created", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    else:
        return Response(
            {
                "status": "failed",
                "message": "invalid data",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


##filter jobs based on diff fields
##add pagination


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def search_jobs_by_title(request, title):
    # use pagination
    jobs = Job.objects.filter(title__icontains=title)
    if jobs.exists():
        paginator = PageNumberPagination()
        paginator.page_size = 5
        paginated_jobs = paginator.paginate_queryset(jobs, request)
        serializer = JobSerializer(paginated_jobs, many=True)
        return paginator.get_paginated_response(
            {
                "status": "success",
                "message": "jobs fetched successfully",
                "data": serializer.data,
            }
        )
    else:
        return Response(
            {
                "status": "success",
                "message": "no jobs found",
                "data": [],
            },
            status=status.HTTP_200_OK,
        )


# anyone can view job
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response(
            {
                "status": "failed",
                "message": "job not found",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    serializer = JobSerializer(job)
    return Response(
        {
            "status": "success",
            "message": "job fetched successfully",
            "data": serializer.data,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_job(request, job_id):
    user_id = request.user.id
    try:
        employer = EmployerProfile.objects.get(user=user_id)
    except EmployerProfile.DoesNotExist:
        return Response(
            {
                "status": "failed",
                "message": "employer of job not found",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response(
            {
                "status": "failed",
                "message": "job not found",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    if employer.id == job.employer.id:
        job.delete()
        return Response(
            {
                "status": "success",
                "message": "job deleted",
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {
                "status": "failed",
                "message": "permission denied",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

# -------------------------------Application----------------------------------------->>>>

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_application(request, job_id):
    user_id = request.user.id
    employee = get_object_or_404(EmployeeProfile, user=user_id)
    job = get_object_or_404(Job, id=job_id)

    # data=request.data.copy()
    # data["employer"]=job.employer.id
    # data["job"]=job.id
    # data["employee"]=employee.id
    # BEST-PRACTICE->
    serializer = ApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(job=job, employee=employee, employer=job.employer)
        return Response(
            {
                "status": "success",
                "message": "Job Application sent",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {
                "status": "failed",
                "message": "invalid data",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    serializer = ApplicationSerializer(application, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "status": "success",
                "message": "application updated successfully",
                "data": serializer.data,
            },
            status=status.HTTP_202_ACCEPTED,
        )
    else:
        return Response(
            {
                "status": "failed",
                "message": "invalid data",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# oldest first - prioritizing early appliers
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_all_applications_on_job(request, job_id):

    job = get_object_or_404(Job, id=job_id)
    applications = Application.objects.filter(job=job).order_by("created_at")
    if request.user == job.employer.user:
        if applications.exists():
            serializer = ApplicationSerializer(applications, many=True)
            return Response(
                {
                    "status": "success",
                    "message": "applications fetched successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": "success",
                    "message": "no application found",
                    "data": [],  # empty list
                },
                status=status.HTTP_200_OK,
            )
    else:
        return Response(
            {
                "status": "failed",
                "message": "unauthorized",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


# get latest first
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_latest_applications_on_job(request, job_id):

    job = get_object_or_404(Job, id=job_id)
    applications = Application.objects.filter(job=job).order_by("-created_at")
    if request.user == job.employer.user:
        if applications.exists():
            serializer = ApplicationSerializer(applications, many=True)
            return Response(
                {
                    "status": "success",
                    "message": "applications fetched successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": "success",
                    "message": "no application found",
                    "data": [],  # empty list
                },
                status=status.HTTP_200_OK,
            )
    else:
        return Response(
            {
                "status": "failed",
                "message": "unauthorized",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


# employee can delete his own application only
@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_application(request, application_id):

    application = get_object_or_404(Application, id=application_id)
    employee_in_application = application.employee
    # employee_in_application = get_object_or_404(EmployeeProfile, id=application.employee)
    employee_in_request = get_object_or_404(EmployeeProfile, user=request.user)
    if employee_in_request == employee_in_application:
        application.delete()
        return Response(
            {
                "status": "success",
                "message": "application deleted",
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {
                "status": "failed",
                "message": "employee can delete his own application only",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
