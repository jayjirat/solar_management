from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import CustomUser
from .serializer import UserSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def home(request):
    return render(request, 'home.html')

def signup(request):
    return render(request, 'signup.html')

@api_view(['GET'])
def get_users(request):
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def register(request):
    """Handles user registration"""
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if not username or not email or not password or not first_name or not last_name:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        validate_email(email)
    except ValidationError:
        return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Account with this email already exits'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Account with this email already exits'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
    custom_user = CustomUser.objects.create(user=user)  # Link User to CustomUser

    serializer = UserSerializer(custom_user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)