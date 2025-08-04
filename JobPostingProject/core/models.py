from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    # default id
    # default password
    ROLES_CHOICES = {"Employee", "Employer"}
    role = models.CharField(role=ROLES_CHOICES)
    email = models.EmailField(unique=True)
    title = models.CharField(
        max_length=150,
        blank=True,
    )


# Best Practice to create seperate profiles for different types of users
class EmployeeProfile:
    company = models.CharField(max_length=100, blank=True,)

    


class EmployerProfile(models.Model):
    file = models.FileField()
   
