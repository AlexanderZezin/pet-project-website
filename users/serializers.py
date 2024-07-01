from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as dj_validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers


def validate_password(password):
    try:
        dj_validate_password(password)
    except ValidationError as error:
        raise serializers.ValidationError(error.messages)
    return password


class RegisterUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, label='Введите пароль')
    password = serializers.CharField(write_only=True, label='Повторите пароль', validators=[validate_password])

    def validate(self, data):
        if data['password1'] != data['password']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password']

    def create(self, validated_data):
        del validated_data['password1']
        return get_user_model().objects.create_user(**validated_data)


class ProfileUserSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True, validators=[validate_password])

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def validate_old_password(self, old_password):
        if not self.instance.check_password(old_password):
            raise serializers.ValidationError("Не верен старый пароль")
        return old_password

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('new_password2'))
        instance.save()
        return instance
