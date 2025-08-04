from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    # default id
    # default password
    ROLE_CHOICES = [
        ("Employee", "Employee"),
        ("Employer", "Employer"),
    ]
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    role = models.CharField(choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    title = models.CharField(
        
        max_length=150,
        blank=True,
    )


# Best Practice to create seperate profiles for different types of users
class EmployeeProfile(models.Model):
    company = models.CharField(max_length=100, blank=True,)

    


class EmployerProfile(models.Model):
    file = models.FileField()
   
