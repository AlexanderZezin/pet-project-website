from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as dj_validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers


class RegisterUserSerializer(serializers.ModelSerializer):
    def validate_password(self, password):
        try:
            dj_validate_password(password)
        except ValidationError as error:
            raise serializers.ValidationError(error.messages)
        return password

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class ProfileUserSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
