import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
import uuid

@pytest.mark.django_db
def test_register_success():
    client = APIClient()
    url = reverse('register')
    username = str(uuid.uuid4())[:10]
    email = f'{str(uuid.uuid4())[:10]}@example.com'
    data = {'username': username, 'email': f'{str(uuid.uuid4())}@example.com', 'password': 'StrongPass1234!'}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username=username).exists()

@pytest.mark.django_db
def test_register_duplicate_email():
    client = APIClient()
    url = reverse('register')
    email = f'{str(uuid.uuid4())[:10]}@example.com'
    User.objects.create_user(username=str(uuid.uuid4())[:10], email=email, password='StrongPass1234!')
    data = {'username': str(uuid.uuid4())[:10], 'email': email, 'password': 'StrongPass1234!'}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data
    assert response.data['email'] == "Email already exists."

@pytest.mark.django_db
def test_register_weak_password():
    client = APIClient()
    url = reverse('register')
    data = {'username': str(uuid.uuid4())[:10], 'email': f'{str(uuid.uuid4())[:10]}@example.com', 'password': '123'}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'password' in response.data
    assert any("This password is too short" in msg for msg in response.data['password'])

@pytest.mark.django_db
def test_login_success():
    client = APIClient()
    url = reverse('login')
    username = str(uuid.uuid4())[:10]
    password = 'StrongPass1234!'
    user = User.objects.create_user(username=username, email=f'{str(uuid.uuid4())[:10]}@example.com', password=password)
    data = {'username': username, 'password': password}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'refresh' in response.data
    assert 'access' in response.data
    # Verify the access token's user_id
    access_token = AccessToken(response.data['access'])
    assert access_token['user_id'] == str(user.id)

@pytest.mark.django_db
def test_login_invalid_credentials():
    client = APIClient()
    url = reverse('login')
    data = {'username': 'nonexistent', 'password': 'wrongpassword'}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['detail'] == 'Invalid username or password.'