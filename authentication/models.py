from django.db import models
from django.contrib.auth.models import User
from enum import Enum

class RoleEnum(Enum):
    ADMIN = 'admin', 'Admin'
    SUPERADMIN = 'superadmin', 'Super Admin'
    DATA_ANALYST = 'data_analyst', 'Data Analyst'
    DRONE_CONTROLLER = 'drone_controller', 'Drone Controller'


# Create your models here.
class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=[(tag.value[0], tag.value[1]) for tag in RoleEnum],
    )

    def __str__(self):
        return self.user.username + " " + self.role