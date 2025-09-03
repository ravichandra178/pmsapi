from django.db import models
from django.contrib.auth.models import User
from rooms.models import Room

class Booking(models.Model):
    STATUS_CHOICES = (
        ('CHECKED_IN', 'Checked In'),
        ('CHECKED_OUT', 'Checked Out'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="User who made the booking.")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, help_text="Booked room.")
    check_in = models.DateTimeField(auto_now_add=True, help_text="Check-in date and time.")
    check_out = models.DateTimeField(null=True, blank=True, help_text="Check-out date and time.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CHECKED_IN', help_text="Booking status.")
    full_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Total price for the booking.")

    def __str__(self):
        return f"Booking {self.id} for Room {self.room.number} by {self.user.username}"