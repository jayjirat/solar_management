from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from .models import CustomUser
import requests
from urllib.parse import urlencode
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
import json
from django.conf import settings
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken


class SocialLoginFacade:
    User = get_user_model()

    def __init__(self, provider):
        self.provider = provider

    def login(self, request):
        if self.provider == 'google':
            return self.google_login(request)
        # elif self.provider == 'facebook':
        #     return self.facebook_login(request)
        else:
            raise ValueError("Unsupported provider")

    def callback(self, request):
        if self.provider == 'google':
            return self.google_callback(request)
        # elif self.provider == 'facebook':
        #     return self.facebook_callback(request)
        else:
            raise ValueError("Unsupported provider")

    def google_login(self, request):
        # Google OAuth2 endpoint
        authorization_endpoint = "https://accounts.google.com/o/oauth2/v2/auth"

        # Get client ID from settings
        client_id = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']

        # Prepare callback URL
        redirect_uri = request.build_absolute_uri('/login/google/callback/')

        # Prepare parameters for authorization request
        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'email profile',
            'access_type': 'offline',
            'include_granted_scopes': 'true',
        }

        # Build authorization URL
        authorization_url = f"{authorization_endpoint}?{urlencode(params)}"

        # Redirect user to authorization URL
        return redirect(authorization_url)

    def google_callback(self, request):
        # Check if there's an error parameter
        if 'error' in request.GET:
            messages.error(
                request, f"Google authentication error: {request.GET['error']}")
            return redirect('login')

        # Get authorization code from request
        code = request.GET.get('code')

        if not code:
            messages.error(
                request, "No authorization code received from Google.")
            return redirect('login')

        # Exchange code for tokens
        token_endpoint = "https://oauth2.googleapis.com/token"
        client_id = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
        client_secret = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['secret']
        redirect_uri = request.build_absolute_uri('/login/google/callback/')

        token_data = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }

        # Get tokens
        token_response = requests.post(token_endpoint, data=token_data)

        if token_response.status_code != 200:
            messages.error(
                request, "Failed to obtain access token from Google.")
            return redirect('login')

        token_json = token_response.json()
        access_token = token_json.get('access_token')

        # Get user info using access token
        userinfo_endpoint = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {'Authorization': f'Bearer {access_token}'}

        userinfo_response = requests.get(userinfo_endpoint, headers=headers)

        if userinfo_response.status_code != 200:
            messages.error(request, "Failed to get user info from Google.")
            return redirect('login')

        userinfo = userinfo_response.json()

        # Extract user data
        email = userinfo.get('email')
        email_verified = userinfo.get('email_verified', False)

        if not email or not email_verified:
            messages.error(
                request, "Google did not provide a verified email address.")
            return redirect('login')

        user = User.objects.filter(email=email).first()
        myuser = None
        # Check if user exists
        if user:
            myuser = CustomUser.objects.get(user=user)
            # User exists, set the backend attribute and log them in
            # Set the backend attribute
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(request, user)  # Now this will work

        # User does not exist, create a new user
        else:
            username = email

            # Check if username already exists and modify if needed
            base_username = username
            count = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{count}"
                count += 1

            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=get_random_string(8)  # Generate a random password
            )

            # Create custom user with default role
            CustomUser.objects.create(
                user=user,
            )
            user = authenticate(request, username=user.username, password=user.password)

            # Set the backend attribute and log in the new user
            # Set the backend attribute
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(request, user)  # Now this will work
        # Generate JWT token
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # You can still use Django's session auth if needed
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(request, user)
        redirect_url = None
        user_role = myuser.role or "user"

        # Set JWT as a cookie
        if(user_role == "admin"):
            redirect_url = "/solar-system/dashboard"
        elif(user_role == "drone_controller"):
            redirect_url = "/solar-system/upload_history"
        elif(user_role == "data_analyst"):
            redirect_url = "/solar-system/reports"
        else:
            redirect_url = "/"


        response = redirect(redirect_url)
        response.set_cookie(
            'access_token', access_token,
            httponly=False,
            secure=True,
            samesite='Lax'
        )

        response.set_cookie(
            'refresh_token', str(refresh),
            httponly=True,
            secure=True,
            samesite='Lax'
        )

        response.set_cookie(
            'username', user.username,
            httponly=True,
            secure=True,
            samesite='Lax'
        )

        response.set_cookie(
            'role', myuser.role,
            httponly=True,
            secure=True,
            samesite='Lax'
        )

        # Redirect to home page
        return response

    # def facebook_login(self, request):
    #     # Facebook OAuth2 endpoint
    #     authorization_endpoint = "https://www.facebook.com/v9.0/dialog/oauth"

    #     # Get client ID from settings
    #     client_id = settings.SOCIALACCOUNT_PROVIDERS['facebook']['APP']['client_id']

    #     # Prepare callback URL
    #     redirect_uri = request.build_absolute_uri('/login/facebook/callback/')

    #     # Prepare parameters for authorization request
    #     params = {
    #         'client_id': client_id,
    #         'redirect_uri': redirect_uri,
    #         'response_type': 'code',
    #         'scope': 'email',
    #     }

    #     # Build authorization URL
    #     authorization_url = f"{authorization_endpoint}?{urlencode(params)}"

    #     # Redirect user to authorization URL
    #     return redirect(authorization_url)

    # def facebook_callback(self, request):
    #     # Check if there's an error parameter
    #     if 'error' in request.GET:
    #         messages.error(request, f"Facebook authentication error: {request.GET['error']}")
    #         return redirect('login')

    #     # Get authorization code from request
    #     code = request.GET.get('code')

    #     if not code:
    #         messages.error(request, "No authorization code received from Facebook.")
    #         return redirect('login')

    #     # Exchange code for access token
    #     token_endpoint = "https://graph.facebook.com/v9.0/oauth/access_token"
    #     client_id = settings.SOCIALACCOUNT_PROVIDERS['facebook']['APP']['client_id']
    #     client_secret = settings.SOCIALACCOUNT_PROVIDERS['facebook']['APP']['secret']
    #     redirect_uri = request.build_absolute_uri('/login/facebook/callback/')

    #     token_data = {
    #         'client_id': client_id,
    #         'redirect_uri': redirect_uri,
    #         'client_secret': client_secret,
    #         'code': code,
    #     }

    #     # Get access token
    #     token_response = requests.get(token_endpoint, params=token_data)

    #     if token_response.status_code != 200:
    #         messages.error(request, "Failed to obtain access token from Facebook.")
    #         return redirect('login')

    #     token_json = token_response.json()
    #     access_token = token_json.get('access_token')

    #     # Get user info using access token
    #     userinfo_endpoint = "https://graph.facebook.com/me?fields=id,name,email"
    #     headers = {'Authorization': f'Bearer {access_token}'}

    #     userinfo_response = requests.get(userinfo_endpoint, headers=headers)

    #     if userinfo_response.status_code != 200:
    #         messages.error(request, "Failed to get user info from Facebook.")
    #         return redirect('login')

    #     userinfo = userinfo_response.json()

    #     # Extract user data
    #     email = userinfo.get('email')

    #     if not email:
    #         messages.error(request, "Facebook did not provide an email address.")
    #         return redirect('login')

    #     user = User.objects.filter(email=email).first()
    #     # Check if user exists
    #     if user:
    #         # User exists, set the backend attribute and log them in
    #         user.backend = 'django.contrib.auth.backends.ModelBackend'  # Set the backend attribute
    #         auth_login(request, user)  # Now this will work

    #     # User does not exist, create a new user
    #     else:
    #         username = email

    #         # Check if username already exists and modify if needed
    #         base_username = username
    #         count = 1
    #         while User.objects.filter(username=username).exists():
    #             username = f"{base_username}{count}"
    #             count += 1

    #         # Create new user
    #         user = User.objects.create_user(
    #             username=username,
    #             email=email,
    #             password=get_random_string(8)  # Generate a random password
    #         )

    #         # Create custom user with default role
    #         CustomUser.objects.create(
    #             user=user,
    #         )

    #         # Log in the new user
    #         user.backend = 'django.contrib.auth.backends.ModelBackend'
    #         auth_login(request, user)

    #     # Redirect to home page
    #     return redirect('home')

    User = get_user_model()


class ThammasatAuthFacade:
    TU_API_URL = "https://restapi.tu.ac.th/api/v1/auth/Ad/verify"
    TU_API_TOKEN = settings.TU_CLIENT_SECRET

    @staticmethod
    def login(request):
        """Handles login process using TU API."""
        try:
            data = json.loads(request.body.decode("utf-8"))
            username = data.get("username")
            password = data.get("password")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        if not username or not password:
            return JsonResponse({"error": "Missing username or password"}, status=400)

        response_data = ThammasatAuthFacade.authenticate(username, password)
        if response_data:
            user = ThammasatAuthFacade.process_user_data(
                username, response_data)
            if user:
                authenticated_user = authenticate(request, username=username, password=password)
                if authenticated_user:
                    auth_login(request, authenticated_user)
                    return JsonResponse(ThammasatAuthFacade.generate_jwt_tokens(authenticated_user), status=200)
                else:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    auth_login(request, user)
                    return JsonResponse(ThammasatAuthFacade.generate_jwt_tokens(user), status=200)
            
        return JsonResponse({"error": "Invalid credentials"}, status=400)

    @staticmethod
    def authenticate(username, password):
        """Send authentication request to TU API."""
        headers = {
            "Content-Type": "application/json",
            "Application-Key": ThammasatAuthFacade.TU_API_TOKEN
        }
        payload = {
            "UserName": username,
            "PassWord": password
        }

        response = requests.post(
            ThammasatAuthFacade.TU_API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def process_user_data(username, response_data):
        """Create or get user from the TU API response data and associate CustomUser."""
        if response_data.get("status") is True:
            email = response_data.get("email")
            name = response_data.get("displayname_en")
            faculty = response_data.get(
                "faculty", response_data.get("organization", ""))
            department = response_data.get("department", "")
            year = 67 - \
                int(username[:2]) + \
                1 if response_data.get("type") == "student" else None

            user, created = User.objects.get_or_create(
                username=name,
                defaults={"email": email, "first_name": name}
            )

            if created:
                user.faculty = faculty
                user.major = department
                if year:
                    user.year = year
                user.save()
                
                # Create associated CustomUser
                CustomUser.objects.create(user=user)
                
            else:
                # Check if CustomUser exists for this user
                try:
                    CustomUser.objects.get(user=user)
                except CustomUser.DoesNotExist:
                    # Create CustomUser if it doesn't exist
                    CustomUser.objects.create(user=user)

            return user
        return None

    @staticmethod
    def generate_jwt_tokens(user):
        """Generate JWT access and refresh tokens for the user."""
        refresh = RefreshToken.for_user(user)
        role = "user"  
        try:
            custom_user = CustomUser.objects.get(user=user)
            if hasattr(custom_user, 'role'):
                role = custom_user.role
        except (CustomUser.DoesNotExist, AttributeError):
            pass  
            
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "faculty": getattr(user, "faculty", ""),
                "major": getattr(user, "major", ""),
                "year": getattr(user, "year", None),
                "displayname_en": getattr(user, "first_name", ""),
                "role": role 
            }
        }
