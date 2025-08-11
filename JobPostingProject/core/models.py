from django.contrib.auth.models import AbstractUser
from django.db import models


##add created_at and updated_at to all models (best practice)
class User(AbstractUser):
    # default id
    # default password
    ROLE_CHOICES = [
        ("Employee", "Employee"),
        ("Employer", "Employer"),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    title = models.CharField(
        max_length=150,
        blank=True,
    )

    # updated_at =
    # created_at =
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Best Practice to create seperate profiles for different types of users
class EmployeeProfile(models.Model):
    file = models.FileField(upload_to="uploads/", null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=11)
    introduction = models.CharField(max_length=1000, blank=True, null=True)


class Skills(models.Model):
    name = models.CharField(max_length=15)
    employee = models.ManyToManyField(EmployeeProfile)


class Experience(models.Model):
    company = models.CharField(max_length=50)
    duration = models.CharField(max_length=20, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    responsibilities = models.CharField(
        max_length=500, blank=True, null=True
    )  # responsiblities
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)


class EmployerProfile(models.Model):
    company = models.CharField(
        max_length=100,
        blank=True,
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=20, blank=True)


class Job(models.Model):
    EXP_CHOICES = [
        ("Internship", "Internship"),
        ("Senior", "Senior"),
        ("Mid-Senior", "Mid-Senior"),
        ("Junior", "Junior"),
        ("Entry", "Entry"),
        ("Executive", "Executive"),
    ]
    WORKPLACE_CHOICES = [
        ("Remote", "Remote"),
        ("Onsite", "Onsite"),
        ("Hybird", "Hybrid"),
    ]
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=2000)
    skills = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=50)
    experience_level = models.CharField(
        max_length=12, choices=EXP_CHOICES, default="entry"
    )
    workplace = models.CharField(
        max_length=8, choices=WORKPLACE_CHOICES, default="onsite"
    )
    number_of_positions = models.IntegerField(blank=True, null=True)


class Application(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    employer = models.OneToOneField(EmployerProfile, on_delete=models.CASCADE)
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    cover_letter = models.CharField(max_length=200, blank=True, null=True)
    cv = models.FileField()
    email = models.EmailField()
    city = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
