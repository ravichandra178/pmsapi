import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rooms.models import Room

@pytest.mark.django_db
def test_room_list_create():
    """Test creating and listing rooms."""
    client = APIClient()
    user = User.objects.create_user(username='user', email='user@example.com', password='User1234!')
    access_token = str(AccessToken.for_user(user))
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    # Create a room
    url = reverse('room-list-create')
    data = {
        'number': '101',
        'price': '100.00',
        'is_available': True
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['is_available'] is True

    # List rooms
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['number'] == '101'

@pytest.mark.django_db
def test_room_detail():
    """Test retrieving, updating, and deleting a room."""
    client = APIClient()
    user = User.objects.create_user(username='user', email='user@example.com', password='User1234!')
    access_token = str(AccessToken.for_user(user))
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    room = Room.objects.create(number='101', price='100.00', is_available=True)

    url = reverse('room-detail', kwargs={'pk': room.id})

    # Retrieve
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['is_available'] is True

    # Update
    data = {
        'number': '101',
        'price': '150.00',
        'is_available': False
    }
    response = client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['is_available'] is False

    # Delete
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Room.objects.count() == 0

@pytest.mark.django_db
def test_room_available_list():
    """Test listing available rooms"""
    client = APIClient()
    user = User.objects.create_user(username='user', email='user@example.com', password='User1234!')
    access_token = str(AccessToken.for_user(user))
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    Room.objects.create(number='101', price='100.00', is_available=True)
    Room.objects.create(number='102', price='150.00', is_available=False)

    url = reverse('room-available-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['number'] == '101'