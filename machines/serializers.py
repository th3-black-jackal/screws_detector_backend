from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Machine

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Machine
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        # keep it simple (no passwords exposed)
        fields = ("id", "username", "first_name", "last_name", "email", "is_staff", "is_active")
        read_only_fields = ("is_staff", "is_active")
