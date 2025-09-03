from django.db import models

# Create your models here.
from django.core.validators import MinValueValidator

class Room(models.Model):
    number = models.CharField(max_length=10, unique=True, help_text="Room number.")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Price per night."
    )
    is_available = models.BooleanField(default=True, help_text="Room availability status.")

    def __str__(self):
        return self.number