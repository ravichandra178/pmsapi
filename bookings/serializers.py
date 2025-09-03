from rest_framework import serializers
from bookings.models import Booking
from bookings.exceptions import validate_booking, PastDateError, InvalidDateRangeError, RoomNotAvailableError
from django.utils import timezone
from rooms.models import Room

class BookingSerializer(serializers.ModelSerializer):
    full_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    room_number = serializers.CharField(write_only=True, required=True, help_text="Room number to be booked.")

    class Meta:
        model = Booking
        fields = ('id', 'user', 'room','room_number', 'check_in', 'check_out', 'status', 'full_price')
        read_only_fields = ('user', 'check_in', 'status', 'full_price')
        extra_kwargs = {
            'room': {'required': False},
            'check_out': {'required': False}
        }

    def validate(self, data):
        room_number = data.get('room_number')
        if not room_number:
            raise RoomNotAvailableError("Room number is required.")
        try:         
            room = Room.objects.get(number=room_number)
            if not room.is_available:
                raise RoomNotAvailableError(f"Room {room_number} is not available.")
        except Room.DoesNotExist:
            raise RoomNotAvailableError(f"Room {room_number} does not exist.")
        
        data['room'] = room    
        check_in = timezone.now()  # Mimic auto_now_add for validation
        check_out = data.get('check_out')
        validate_booking(data.get('room'), check_in, check_out, instance=self.instance)
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        room_number = validated_data.pop('room_number', None)
        validated_data['room'] = Room.objects.get(number=room_number)
        return super().create(validated_data)