from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        read_only_fields = ["created_at", "updated_at"]

    def __str__(self):
        return f"{self.first_name} + {self.last_name}"

    def validate(self, data):

        username = data["username"]
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("username already exists")

        return data

class UpdateUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=['__all__']
        read_only_fields=['created_at','updated_at']
    
    def validate(self,data):
        
        pass