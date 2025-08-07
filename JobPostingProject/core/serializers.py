from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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
        model = User
        fields = ["__all__"]
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, data):

        first_name = data.GET.get("first_name", "")
        last_name = data.GET.get("last_name", "")
        role = data.GET.get("role", "")
        username = data.GET.get("username", "")
        email = data.GET.get("email", "")
        title = data.GET.get("title", "")
        if not first_name:
            raise serializers.ValidationError("first name cannot be empty")
        if not last_name:
            raise serializers.ValidationError("last name cannot be empty")
        if not role:
            raise serializers.ValidationError("role cannot be empty")
        if not username:
            raise serializers.ValidationError("username cannot be empty")
        if not email:
            raise serializers.ValidationError("email cannot be empty")
        if username == User.objects.filter(username=username).exists():
            raise serializers.ValidationError("username already exists")
        return data


class EmployeeProfileSerializer:
    class Meta:
        model = EmployeeProfile
        fields = ["__all__"]

    # file field validator
    def validate():
        pass


class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["__all__"]

    def validate(self, data):
        company = data.GET.get("company", "")
        if not company:
            raise serializers.ValidationError("company cannot be empty")
        return data


class JobSerializer(serializers.ModelSerializer):
    pass


class ApplicationSerializer(serializers.ModelSerializer):
    pass


class SkillsSerializer(serializers.ModelSerializer):
    pass


class ExperienceSerializer(models.ModelSerializer):
    pass
