from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# 1. Custom Manager to handle email-based login
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# 2. Your Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )

    # Remove username, use email instead
    username = None
    email = models.EmailField(unique=True)
    
    # Common Fields
    full_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    terms_accepted = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    # Teacher specific fields
    institution_name = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    employee_id = models.CharField(max_length=50, blank=True, null=True)

    # Student specific fields
    roll_number = models.CharField(max_length=50, blank=True, null=True)
    course_year = models.CharField(max_length=20, blank=True, null=True)
    section_batch = models.CharField(max_length=50, blank=True, null=True)

    objects = UserManager() # Connect the custom manager

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'role']

    def __str__(self):
        return f"{self.email} ({self.role})"