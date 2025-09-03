from rest_framework import serializers
from django.contrib.auth.models import User
from authentication.exceptions import DuplicateEmailError, PasswordValidationError, InvalidCredentialsError
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'email': {'required': True, 'help_text': 'Required. Enter a valid email address.'},
            'username': {'required': True, 'help_text': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'},
            'password': {'required': True, 'write_only': True, 'style': {'input_type': 'password'}, 'help_text': 'Required. At least 8 characters.'}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise DuplicateEmailError()
        return value

    def validate_password(self, value):
        if value is None or value == '':
            raise InvalidCredentialsError("Password cannot be null or empty.")
        try:
            validate_password(value, user=None)
        except Exception as e:
            raise PasswordValidationError(str(e))
        return value

    def validate(self, data):
        if 'password' not in data or data['password'] is None:
            raise InvalidCredentialsError("Password cannot be null.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})