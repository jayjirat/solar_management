from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser, RoleEnum
from .models import CustomUser, EmailOTP


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")

        try:
            user = User.objects.get(email=email)
            email_otp = EmailOTP.objects.get(user=user)

            if not email_otp.is_valid():
                raise serializers.ValidationError({"otp": "OTP has expired."})

            if email_otp.otp != otp:
                raise serializers.ValidationError({"otp": "Invalid OTP."})
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "User with this email does not exist."})
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError({"otp": "No OTP found for this user."})

        return data