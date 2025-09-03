from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bookings.models import Booking
from bookings.serializers import BookingSerializer
from django.utils import timezone
from django.http import Http404
from math import ceil

class CheckinView(ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related('user', 'room')

    def perform_create(self, serializer):
        booking = serializer.save()
        booking.room.is_available = False
        booking.room.save()

class BookingDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related('user', 'room')

    def perform_update(self, serializer):
        old_booking = self.get_object()
        booking = serializer.save()
        if old_booking.room != booking.room:
            old_booking.room.is_available = True
            old_booking.room.save()
            booking.room.is_available = False
            booking.room.save()

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.room.is_available = True
            instance.room.save()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({"detail": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

class CheckOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            room_number = request.data.get('room_number')
            booking = Booking.objects.select_related('room').get(user=request.user, room__number=room_number, status='CHECKED_IN')
        except Booking.DoesNotExist:
            return Response({"detail": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)
        
        booking.check_out = timezone.now()
        booking.status = 'CHECKED_OUT'
        # Calculate full_price: room.price * number of nights (minimum 1)
        nights = (booking.check_out - booking.check_in).days or 1
        booking.full_price = booking.room.price * nights
        booking.room.is_available = True
        booking.room.save()
        booking.save()
        serializer = BookingSerializer(booking, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)