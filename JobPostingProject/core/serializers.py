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
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, data):

        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        role = data.get("role", "")
        username = data.get("username", "")
        email = data.get("email", "")
        title = data.get("title", "")
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


class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = "__all__"


class UpdateEmployeeSerializer(serializers.ModelSerializer):
    fields = "__all__"
    read_only_fields = ["user"]

    def validate(self, data):
        city = data.get("city", "")
        phone_number = data.get("phone_number", "")
        if not city:
            return serializers.ValidationError("city cannot be empty")
        if not phone_number:
            return serializers.ValidationError("phone number cannot be empty")
        return data


class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"

    def validate(self, data):
        company = data.GET.get("company", "")
        if not company:
            raise serializers.ValidationError("company cannot be empty")
        return data


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model: Job
        fields = "__all__"
        read_only_fields = ["created_at"]

    def validate(self, data):
        title = data.GET.get("title", "")
        description = data.GET.get("description", "")
        # skills=data.GET.get("skills","")
        # location=data.GET.get("location","")
        number = data.GET.get("number_of_positions", "")

        if not title:
            raise serializers.ValidationError("title cannot be empty")
        if not description:
            raise serializers.ValidationError("description cannot be empty")
        if number < 0:
            raise serializers.ValidationError("number cannot be negative")
        return data


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, data):
        email = data.GET.get("email", "")
        city = data.GET.get("city", "")
        employee_id = data.GET.get("employee", "")
        employer_id = data.GET.get("employer", "")
        job_id = data.GET.get("job", "")
        if not email:
            raise serializers.ValidationError("email not found")
        if not city:
            raise serializers.ValidationError("city", "")
        # cannot apply if application already exists


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = "__all__"

    def validate(self, data):
        name = data.GET.get("name", "")
        if not name:
            raise serializers.ValidationError("Skill cannot be empty")
        return data


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"

    def validate(self, data):
        company = data.GET.get("company", "")
        start_date = data.GET.get("start_date", "")
        end_date = data.GET.get("end_date", "")
        responsibilities = data.GET.get("responsibilities", "")
        if not company:
            raise serializers.ValidationError("company cannot be empty")
        if not start_date:
            raise serializers.ValidationError("start date cannot be empty")
        if start_date > end_date:
            raise serializers.ValidationError(
                "start date cannot be greater than end date"
            )
        return data
