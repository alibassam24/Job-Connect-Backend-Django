from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authentication import authenticate
# Create your views here.
@api_view(["POST"])
def register_user(request):
    email= request.data["username"]
    password=request.data["password"]
    
    serializer=UserSerializer(data=request.data)
    if serializer.is_valid():
        
        user=serializer.save()
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return Response({"status":"success","message":"user created successfully","Data":serializer.data}, status=status.HTTP_201_CREATED,)
    
    else:
        return Response({"status":"failed","message":"Invalid data","Error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
def login_user(request):
    
    username=request.data["username"]
    password=request.data["password"]
    
    user=authenticate(username=username,password=password)

    if user:
        token , _ = Token.objects.get_or_create()
        return Response({"status":"success","message":"login successful","Token":token.key},status=status.HTTP_200_OK,)
    else: 
        return Response ({"status":"failed","message":"Invalid data"},status=status.HTTP_400_BAD_REQUEST,)
