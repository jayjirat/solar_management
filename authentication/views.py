from django.http import JsonResponse
import requests
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
import json

def home(request):
    return render(request, 'home.html') 


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