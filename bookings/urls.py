# bookings/urls.py
from django.urls import path
from bookings.views import CheckinView, BookingDetailView, CheckOutView

urlpatterns = [
    path('', CheckinView.as_view(), name='booking-list-create'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('checkout/', CheckOutView.as_view(), name='booking-checkout'),
]