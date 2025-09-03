import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rooms.models import Room
from bookings.models import Booking
from django.utils import timezone
from datetime import timedelta
from bookings.exceptions import InvalidDateRangeError, PastDateError, RoomNotAvailableError

@pytest.mark.django_db
def test_checkin_view():
    """Test creating and listing bookings."""
    client = APIClient()
    user = User.objects.create_user(username='user', email='user@example.com', password='User1234!')
    access_token = str(AccessToken.for_user(user))
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    room = Room.objects.create(number='101', price='100.00')  # is_available=True by default

    url = reverse('booking-list-create')
    data = {
        "room_number": "101"
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['status'] == 'CHECKED_IN'
    assert Room.objects.get(id=room.id).is_available is False

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['room'] == room.id

@pytest.mark.django_db
def test_booking_detail():
    """Test retrieving, updating, and deleting a booking."""
    client = APIClient()
    user = User.objects.create_user(username='user', email='user@example.com', password='User1234!')
    access_token = str(AccessToken.for_user(user))
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    room = Room.objects.create(number='101', price='100.00')  # is_available=True by default
    url = reverse('booking-list-create')
    data = {"room_number": "101"}
    response = client.post(url, data, format='json')  # Create via API to set is_available=False
    booking_id = response.data['id']
    assert response.data['full_price'] == '0.00'

    url = reverse('booking-detail', kwargs={'pk': booking_id})

    # Retrieve
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == 'CHECKED_IN'

    # Update
    room2 = Room.objects.create(number='102', price='150.00')  # is_available=True by default
    data = {
        "room_number": "102",
        "check_out": (timezone.now() + timedelta(days=2)).isoformat()
    }
    response = client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == 'CHECKED_IN'
    assert Room.objects.get(id=room.id).is_available is True
    assert Room.objects.get(id=room2.id).is_available is False

    # Delete
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Room.objects.get(id=room2.id).is_available is True

@pytest.mark.django_db
def test_checkout_view():
    """Test checking out a booking."""
    client = APIClient()
    user = User.objects.create_user(username='user', email='user@example.com', password='User1234!')
    access_token = str(AccessToken.for_user(user))
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    room = Room.objects.create(number='101', price='100.00')  # is_available=True by default
    url = reverse('booking-list-create')
    data = {"room_number": "101"}
    response = client.post(url, data, format='json')
    assert response.data['full_price'] == '0.00'

    url = reverse('booking-checkout')
    data = {"room_number": "101"}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['status'] == 'CHECKED_OUT'
    assert response.data['check_out'].startswith(timezone.now().date().isoformat())
    assert response.data['full_price'] == '100.00'
    assert Room.objects.get(id=room.id).is_available is True

@pytest.mark.django_db
def test_checkout_invalid_room_number():
    """Test checking out with invalid room_number."""
    client = APIClient()
    user = User.objects.create_user(username='user', email='user@example.com', password='User1234!')
    access_token = str(AccessToken.for_user(user))
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    Room.objects.create(number='101', price='100.00')  # is_available=True by default
    url = reverse('booking-checkout')
    data = {"room_number": "999"}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'] == 'Booking not found.'

@pytest.mark.django_db
def test_checkout_no_active_booking():
    """Test checking out with no active booking."""
    client = APIClient()
    user = User.objects.create_user(username='user', email='user@example.com', password='User1234!')
    access_token = str(AccessToken.for_user(user))
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    Room.objects.create(number='101', price='100.00')  # is_available=True by default
    url = reverse('booking-checkout')
    data = {"room_number": "101"}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'] == 'Booking not found.'