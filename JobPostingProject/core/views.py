from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *

# Create your views here.


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


@api_view(["GET"])
def login_user(request):

    username = request.data["username"]
    # username = request.data.get("username", "")
    password = request.data["password"]

    user = authenticate(username=username, password=password)

    if user:
        token, _ = Token.objects.get_or_create()
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
                {"status": "failed", "message": "User not found", "id": user.id},
                status=status.HTTP_400_BAD_REQUEST,
            )
