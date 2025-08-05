from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    # default id
    # default password
    ROLE_CHOICES = [
        ("Employee", "Employee"),
        ("Employer", "Employer"),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(choices=ROLE_CHOICES)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    title = models.CharField(
        max_length=150,
        blank=True,
    )


# Best Practice to create seperate profiles for different types of users
class EmployeeProfile(models.Model):
    company = models.CharField(
        max_length=100,
        blank=True,
    )
    employee_id=models.ForeignKey(User, to_field="id",on_delete=models.CASCADE)


class EmployerProfile(models.Model):
    file = models.FileField()
    employer_id=models.ForeignKey(User, to_field="id",on_delete=models.CASCADE)
