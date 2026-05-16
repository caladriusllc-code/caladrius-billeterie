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
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'date_of_birth', 'adress', 'city', 
            'country', 'is_verified'
        ]
        read_only_fields = ['id', 'is_verified']


# ========== SERIALIZER POUR L'ORGANISATEUR ==========
class OrganisateurSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription d'un organisateur
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone_number', 'city', 'country'
        ]
        read_only_fields = ['id', 'is_verified']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {"password_confirm": _("Les mots de passe ne correspondent pas.")}
            )
        return attrs
    
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("Cet email est déjà utilisé."))
        return value
    
    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError(_("Ce nom d'utilisateur est déjà pris."))
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            city=validated_data.get('city', ''),
            country=validated_data.get('country', ''),
        )
        
        user.role = 'organisateur'
        user.is_organisateur = True
        user.is_verified = False
        user.save()
        
        return user


# ========== SERIALIZER POUR L'UTILISATEUR NORMAL ==========
class UtilisateurSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription d'un utilisateur normal (API REST)
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone_number', 'date_of_birth',
            'adress', 'city', 'country'
        ]
        read_only_fields = ['id', 'is_verified']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {"password_confirm": _("Les mots de passe ne correspondent pas.")}
            )
        return attrs
    
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("Cet email est déjà utilisé."))
        return value
    
    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError(_("Ce nom d'utilisateur est déjà pris."))
        return value
    
    def validate_date_of_birth(self, value):
        if value and value > datetime.date.today():
            raise serializers.ValidationError(_("La date de naissance ne peut pas être dans le futur."))
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            date_of_birth=validated_data.get('date_of_birth', None),
            address=validated_data.get('address', ''),
            city=validated_data.get('city', ''),
            country=validated_data.get('country', ''),
        )
        
        user.role = 'utilisateur'
        user.is_organisateur = False
        user.is_verified = False
        user.save()
        
        return user