from rest_framework.exceptions import APIException
from rest_framework import status
from django.contrib.auth.password_validation import validate_password

class PasswordValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'invalid_password'

    def __init__(self, password, user=None):
        try:
            validate_password(password, user=user)
            self.detail = {}  # No error if validation passes
        except Exception as e:
            self.detail = {'password': list(e.messages)}

class DuplicateEmailError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {"email": "Email already exists."}
    default_code = 'duplicate_email'

class InvalidCredentialsError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Invalid username or password.'
    default_code = 'invalid_credentials'