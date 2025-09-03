from rest_framework import serializers
from rooms.models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'number', 'price', 'is_available')
        extra_kwargs = {
            'number': {'required': True},
            'price': {'required': True},
            'is_available': {'required': True}
        }