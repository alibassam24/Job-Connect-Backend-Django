from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (api_view, authentication_classes,
                                       parser_classes, permission_classes)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *

# Create your views here.

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
def get_skills_by_id(request, id):
    pass


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_skills(request):
    pass


# -------------------------------Experience----------------------------------------->>>>


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_experience(request):
    pass


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_experience_by_id(request, id):
    pass


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_experience(request):
    pass


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_experience(request, experience_id):
    pass


# -------------------------------Job----------------------------------------->>>


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_job(request):
    pass


@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_job(request):
    pass


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def search_jobs(request):
    pass


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_job(request):
    pass


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_job(request):
    pass


##filter jobs based on diff fields
##add pagination

# -------------------------------Application----------------------------------------->>>>


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_application(request):
    pass


@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_application(request):
    pass


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_application(request):
    pass


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_application():
    pass
