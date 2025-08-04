from rest_framework import serializers
from .models import *
from rest_framework.validators import ValidationError


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['__all__']
        read_only_fields=['created_at','updated_at']

    def __str__(self):
        return f"{self.first_name} + {self.last_name}"
    
    def validate(self, data):
        email=data["email"]

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exits")


        username=data["username"]

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("username already exists")

        return data
    