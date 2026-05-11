from rest_framework import serializers
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class CustomerClassSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'date_of_birth',
            'adress',
            'city',
            'country',
            'is_verified'
        ]
        reafd_only_fields = ['id', 'is_verified']