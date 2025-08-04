from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from serializers import *


# Create your views here.
@api_view[("POST")]
def register_user(request):
    email= request.data["email"]
    password=request.data["password"]
    
    serializer=UserSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.set_password(password)
        serializer.save()
        return Response({"status":"success","message":"user created successfully","Data":serializer.data}, status=status.HTTP_201_CREATED,)
    
    else:
        return Response({"status":"success","message":"Invalid data","Error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)