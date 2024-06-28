from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as dj_validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def validate_password(self, password):
        try:
            dj_validate_password(password)
        except ValidationError as error:
            raise serializers.ValidationError(error.messages)
        return password

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class ProfileUserSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=False)
    new_password1 = serializers.CharField(required=False)
    new_password2 = serializers.CharField(required=False)

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def validate_old_password(self, old_password):
        if not self.instance.check_password(old_password):
            raise serializers.ValidationError("Не верен старый пароль")
        return old_password

    def validate_new_password2(self, password):
        try:
            dj_validate_password(password)
        except ValidationError as error:
            raise serializers.ValidationError(error.messages)
        return password

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('new_password2'))
        instance.save()
        return instance
