from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_customer = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    other_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.email} - {self.other_name}"

    def age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            if (today.month, today.day) < (
                self.date_of_birth.month,
                self.date_of_birth.day,
            ):
                age -= 1
            return age
        return None
