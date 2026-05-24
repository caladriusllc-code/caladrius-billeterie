import datetime  
from rest_framework import serializers
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password


# ========== SERIALIZER EXISTANT ==========
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
            'address', 
            'city', 
            'country', 
            'is_verified',
            'password'
        ]
        read_only_fields = ['id', 'is_verified']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)   # Hash le mot de passe
        user.save()
        return user
