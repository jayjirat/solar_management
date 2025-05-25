from django.db import models
from django.contrib.auth.models import User
from enum import Enum
import random
from django.utils.timezone import now
from datetime import timedelta


class RoleEnum(Enum):
    USER = 'user', 'User'
    ADMIN = 'admin', 'Admin'
    SUPERADMIN = 'superadmin', 'Super Admin'
    DATA_ANALYST = 'data_analyst', 'Data Analyst'
    DRONE_CONTROLLER = 'drone_controller', 'Drone Controller'

class StatusEnum(Enum):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'

# Create your models here.
class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom')
    role = models.CharField(
    max_length=20,
    choices=[(tag.value[0], tag.value[1]) for tag in RoleEnum],
    default=RoleEnum.USER.value[0],
    )
    status = models.CharField(
    max_length=20,
    choices=[(tag.value[0], tag.value[1]) for tag in StatusEnum],
    default=StatusEnum.ACTIVE.value[0],
    )
    display_name = models.CharField(max_length=150, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        role = self.role if self.role else "user"
        return f"{self.user.username} role: {role} display name: {self.display_name} profile image: {self.profile_image}" 


class EmailOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)

    def is_valid(self):
        """Check if the OTP is still valid (5 minutes expiration)"""
        return self.created_at >= now() - timedelta(minutes=5)

    @staticmethod
    def generate_otp():
        """Generate a 6-digit random OTP"""
        return str(random.randint(100000, 999999))
