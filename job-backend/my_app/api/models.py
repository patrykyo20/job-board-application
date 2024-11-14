from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
        
    age = models.IntegerField(null=True, blank=True)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True)
    jobApplication = models.ForeignKey('Job', on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='job_applications')
    jobOfferPosted = models.ForeignKey('Job', on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='job_offers')
    createdAt = models.DateTimeField(auto_now_add=True)
    changedAt = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name or self.email.split('@')[0]

    def get_short_name(self):
        return self.name or self.email.split('@')[0]


class Location(models.Model):
    TYPE_OF_JOB = [
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
        ('Office', 'Office'),
    ]  

    city = models.CharField(max_length=100)
    postalCode = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    jobType = models.CharField(
        max_length=255,
        choices=TYPE_OF_JOB,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.city}, {self.country}"

class Salary(models.Model):
    hourly = models.CharField(max_length=10, blank=True, null=True)
    monthly = models.CharField(max_length=20, blank=True, null=True)
    yearly = models.CharField(max_length=30, blank=True, null=True)
    
class Image(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="media")

class Job(models.Model):
    EXPERIENCE = [
        ('Intern', 'Intern'),
        ('Junior', 'Junior'),
        ('Regular', 'Regular'),
        ('Senior', 'Senior'),
        ('Staff', 'Staff'),
    ]  

    TIME_DIMENSION = [
        ('Full-Time', 'Full-Time'),
        ('Part-Time', 'Part-Time'),
    ]  

    position = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    image = models.ForeignKey('Image', on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, null=True, blank=True)
    salary = models.ForeignKey('Salary', on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    experience = models.CharField(max_length=30, choices=EXPERIENCE)
    timeDimension = models.CharField(max_length=30, choices=TIME_DIMENSION)
    isPremium = models.BooleanField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    changedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.position} at {self.company}"
