from rest_framework.exceptions import ValidationError
from django.utils import timezone

class InvalidDateRangeError(ValidationError):
    default_detail = "Check-out date must be after check-in date."
    default_code = 'invalid_date_range'

class PastDateError(ValidationError):
    default_detail = "Check-in date cannot be in the past."
    default_code = 'past_date'

class RoomNotAvailableError(ValidationError):
    default_detail = "Room is not available."
    default_code = 'room_not_available'

def validate_booking(room, check_in, check_out, instance=None):
    """Validate booking"""
    if not check_in:
        check_in = timezone.now()  # Mimic auto_now_add
    if not (check_in.date() >= timezone.now().date()):
        raise PastDateError()
    # Refresh room
    room = room.__class__.objects.get(pk=room.pk)
    if not room.is_available:
        raise RoomNotAvailableError()
    if check_out and not (check_in < check_out):
        raise InvalidDateRangeError()
