from django.shortcuts import render 
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CustomerClassSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import OrganisateurSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UtilisateurSerializer



# Create your views here.
def home(request):
    return HttpResponse("Hello, World!")


class CreateUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomerClassSerializer(data=request.data)

        try:
            if serializer.is_valid():
                user = serializer.save()
                return Response(
                    {
                        "user": serializer.data,
                        'message': _("Votre compte a été créé avec succès.")
                    }, 
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {
                        "errors": serializer.errors,
                        'message': _("La création du compte a échoué. Veuillez vérifier les données fournies.")
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {
                    "error": str(e),
                    'message': _("Une erreur inattendue s'est produite lors de la création du compte.")
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrganisateurRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OrganisateurSerializer(data=request.data)

        try: 
            if serializer.is_valid(): 
                user = serializer.save()
                refresh = RefreshToken.for_user(user)

                return Response(
                    {
                        "success": True,
                        "message": _("Votre compte organisateur a été créé avec succès."),
                        "user": {
                            "id": str(user.id),
                            "username": user.username,
                            "email": user.email,
                            "role": user.role,
                            "is_organisateur": user.is_organisateur
                        },
                        "tokens": {
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
                        }
                    }, 
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response( 
                    {
                        "success": False,
                        "errors": serializer.errors,
                        "message": _("La création du compte organisateur a échoué.")
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "error": str(e),
                    "message": _("Une erreur inattendue s'est produite.")
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrganisateurLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {
                    "success": False,
                    "message": _("Veuillez fournir un nom d'utilisateur/email et un mot de passe.")
                },
                status=status.HTTP_400_BAD_REQUEST
            )
       
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_organisateur:
            if not user.is_active:
                return Response(
                    {
                        "success": False,
                        "message": _("Votre compte est désactivé. Contactez l'administrateur.")
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            refresh = RefreshToken.for_user(user)
            
            return Response(
                {
                    "success": True,
                    "message": _(f"Bienvenue {user.username} !"),
                    "user": {
                        "id": str(user.id),
                        "username": user.username,
                        "email": user.email,
                        "role": user.role,
                        "is_organisateur": user.is_organisateur,
                        "organisation_name": getattr(user, 'organisation_name', None)
                    },
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "success": False,
                    "message": _("Nom d'utilisateur/email ou mot de passe incorrect, ou vous n'êtes pas organisateur.")
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


class OrganisateurDashboardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        if not user.is_organisateur:
            return Response(
                {
                    "success": False,
                    "message": _("Accès non autorisé. Cette page est réservée aux organisateurs.")
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        dashboard_data = {
            "success": True,
            "organisateur": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "phone_number": user.phone_number,
                "organisation_name": getattr(user, 'organisation_name', None),
                "city": user.city,
                "country": user.country,
                "is_verified": user.is_verified,
                "date_joined": user.date_joined,
            },
            "statistiques": {
                "total_events": 0,
                "total_participants": 0,
                "total_revenue": 0,
            },
            "recent_activities": []
        }
        
        return Response(dashboard_data, status=status.HTTP_200_OK)


class OrganisateurLogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response(
                {
                    "success": True,
                    "message": _("Vous avez été déconnecté avec succès.")
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": _("Erreur lors de la déconnexion.")
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class CheckAuthStatusView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        return Response(
            {
                "success": True,
                "is_authenticated": True,
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "is_organisateur": user.is_organisateur,
                    "is_verified": user.is_verified,
                }
            },
            status=status.HTTP_200_OK
        )
    

class UtilisateurRegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UtilisateurSerializer(data=request.data)  # ← Utiliser serializer
        
        try:
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "success": True,
                        "message": _("Votre compte a été créé avec succès."),
                        "user": {
                            "id": str(user.id),
                            "username": user.username,
                            "email": user.email,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "role": user.role,
                            "is_organisateur": user.is_organisateur
                        },
                        "tokens": {
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
                        }
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {
                        "success": False,
                        "errors": serializer.errors,
                        "message": _("La création du compte a échoué.")
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "error": str(e),
                    "message": _("Une erreur inattendue s'est produite.")
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UtilisateurLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {
                    "success": False,
                    "message": _("Veuillez fournir un nom d'utilisateur/email et un mot de passe.")
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and not user.is_organisateur:
            if not user.is_active:
                return Response(
                    {
                        "success": False,
                        "message": _("Votre compte est désactivé.")
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            refresh = RefreshToken.for_user(user)
            
            return Response(
                {
                    "success": True,
                    "message": _(f"Bienvenue {user.username} !"),
                    "user": {
                        "id": str(user.id),
                        "username": user.username,
                        "email": user.email,
                        "role": user.role,
                        "is_organisateur": user.is_organisateur
                    },
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "success": False,
                    "message": _("Nom d'utilisateur/email ou mot de passe incorrect.")
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


class UtilisateurProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user

        
        if user.is_organisateur:
            return Response(
                {
                    "success": False,
                    "message": _("Cette page est réservée aux utilisateurs.")
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        return Response(
            {
                "success": True,
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone_number": user.phone_number,
                    "date_of_birth": user.date_of_birth,
                    "address": user.address,  
                    "city": user.city,
                    "country": user.country,
                    "is_verified": user.is_verified,
                    "date_joined": user.date_joined,
                }
            },
            status=status.HTTP_200_OK
        )
    
    def put(self, request):
        user = request.user
        
        if user.is_organisateur:
            return Response(
                {"success": False, "message": _("Non autorisé")},
                status=status.HTTP_403_FORBIDDEN
            )
        
        editable_fields = ['first_name', 'last_name', 'phone_number','date_of_birth', 'address', 'city', 'country'] 
        
        for field in editable_fields:
            if field in request.data:
                setattr(user, field, request.data[field])
        
        user.save()
        
        return Response(
            {
                "success": True,
                "message": _("Profil mis à jour avec succès."),
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone_number": user.phone_number,
                }
            },
            status=status.HTTP_200_OK
        )