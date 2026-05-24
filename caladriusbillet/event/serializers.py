from .models import Event
from rest_framework import serializers
from account.serializers import CustomerClassSerializer

class EventSerializer(serializers.ModelSerializer):

    organizer = CustomerClassSerializer(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'organizer',
            'description',
            'category',
            'venue_name',
            'address',
            'city',
            'country',
            'latitude',
            'longitude',
            'capacity',
            'start_date',
            'end_date',
            'sales_start_date',
            'sales_end_date',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        # request.user est garanti authentifié par la permission
        return Event.objects.create(organizer=request.user, **validated_data)