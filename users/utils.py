from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User


def create_user_account(email, password, first_name="", last_name="", **extra_fields):
    user = User.objects.create_user(
        email=email, password=password, first_name=first_name,
        last_name=last_name, **extra_fields)
    return user


def get_and_authenticate_user(email, password):
    user = authenticate(username=email, password=password)
    if user is None:
        raise serializers.ValidationError("Invalid username/password. Please try again!")
    return user
