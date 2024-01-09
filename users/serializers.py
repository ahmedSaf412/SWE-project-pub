from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.contrib.auth import authenticate
from .models import Applicant


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the user
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')

    def validate_email(self, value):
        user = User.objects.filter(email=value).exists()
        if user:
            raise serializers.ValidationError("Email is already taken")
        return value

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError("Invalid username/password. Please try again!")
        data['user'] = user
        return data


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'auth_token')
        read_only_fields = ('id', 'is_active', 'is_staff')

    def get_auth_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key


class EmptySerializer(serializers.Serializer):
    pass


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Current password does not match')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        exclude = ['branch', 'emp', 'appointment', 'documents']  # Exclude the foreign key fields

