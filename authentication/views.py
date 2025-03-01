from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from .models import CustomUser, EmailOTP
from .serializers import UserSerializer, SendOTPSerializer, VerifyOTPSerializer, LoginSerializer
from rest_framework.decorators import api_view, APIView
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import logout
from django.http import JsonResponse
import requests
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .facade import SocialLoginFacade

import json



def home(request):
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@ensure_csrf_cookie
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Or some other URL
    return render(request, 'login.html')


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'username': user.username
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token
            return Response({"message": "Logout successful"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

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


def google_login(request):
    facade = SocialLoginFacade('google')
    return facade.login(request)

def google_callback(request):
    facade = SocialLoginFacade('google')
    return facade.callback(request)

def facebook_login(request):
    facade = SocialLoginFacade('facebook')
    return facade.login(request)

def facebook_callback(request):
    facade = SocialLoginFacade('facebook')
    return facade.callback(request)



User = get_user_model()

TU_API_URL = "https://restapi.tu.ac.th/api/v1/auth/Ad/verify"
TU_API_TOKEN = "TU6796d72157595c2542172d677bb9ec0698c85e30a68dcf7fb3a5110c17c63d6c8341443a63f63b1170ba569bd9e9896f"

@method_decorator(csrf_exempt, name='dispatch')
class ThammasatLoginAPI(APIView):
    def get(self, request):
        return JsonResponse({"message": "TU API Webhook is connected!"}, status=200)

    def post(self, request):
        print("POST request received!")
        print("Request Data:", request.body)

        try:
            data = json.loads(request.body.decode("utf-8"))
            username = data.get("username")
            password = data.get("password")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        headers = {
            "Content-Type": "application/json",
            "Application-Key": TU_API_TOKEN
        }
        payload = {
            "UserName": username,
            "PassWord": password
        }

        response = requests.post(TU_API_URL, json=payload, headers=headers)
        print("TU API Status Code:", response.status_code)
        print("TU API Response:", response.text)

        if response.status_code == 200:
            response_data = response.json()

            if response_data.get("status") is True:
                # Extract User Info
                email = response_data.get("email")
                name = response_data.get("displayname_en")
                faculty = response_data.get("faculty", response_data.get("organization", ""))
                department = response_data.get("department", "")
                year = 67 - int(username[:2]) + 1 if response_data.get("type") == "student" else None

                # Create or Get User
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={"email": email, "first_name": name}
                )

                if created:
                    user.faculty = faculty
                    user.major = department
                    if year:
                        user.year = year
                    user.save()

                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "faculty": faculty,
                        "major": department,
                        "year": year
                    }
                }, status=200)

        return JsonResponse({"error": "Invalid credentials"}, status=400)