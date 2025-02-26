from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser, RoleEnum


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
