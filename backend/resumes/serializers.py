from django.contrib.auth.models import User
from rest_framework import serializers
from .models import CV

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = ("id", "title", "language", "template", "data", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
    def validate_data(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("CV data must be a JSON object.")
        return value
