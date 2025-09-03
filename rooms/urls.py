from django.urls import path
from rooms.views import RoomListCreateView, RoomDetailView, RoomAvailableListView

urlpatterns = [
    path('', RoomListCreateView.as_view(), name='room-list-create'),
    path('<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('available/', RoomAvailableListView.as_view(), name='room-available-list'),
]