from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import CustomUser, EmailOTP
from .serializer import UserSerializer, SendOTPSerializer, VerifyOTPSerializer
from rest_framework.decorators import api_view, APIView
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail


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
    
    user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, is_active=False)
    custom_user = CustomUser.objects.create(user=user)  # Link User to CustomUser

    serializer = UserSerializer(custom_user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

class SendOTPView(APIView):
    """Send OTP to user's email"""

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)

            # Generate and save OTP
            otp = EmailOTP.generate_otp()
            EmailOTP.objects.update_or_create(user=user, defaults={"otp": otp})

            # Send OTP via email
            send_mail(
                "Your OTP Code",
                f"Your OTP code is {otp}. It is valid for 5 minutes.",
                "6510615062@student.tu.ac.th",
                [email],
                fail_silently=False,
            )

            return Response({"message": "OTP sent successfully!"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    """Verify OTP"""

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)

            # Activate user and delete OTP
            user.is_active = True
            user.save()
            EmailOTP.objects.get(user=user).delete()

            return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)
        error_message = serializer.errors
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST) 

def verify_account(request):
    return render(request, 'verify_account.html')