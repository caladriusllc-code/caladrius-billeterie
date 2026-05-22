from django.shortcuts import render 
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CustomerClassSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

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

class LoginView(APIView):
    
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        # Vérification des champs obligatoires
        if not password:
            return Response(
                {'error': 'Veuillez fournir un mot de passe.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not email and not username:
            return Response(
                {'error': 'Veuillez fournir un email ou un nom d\'utilisateur.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Authentification par email
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                username = user.username  # On récupère le username pour l'authentification
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'Email ou mot de passe incorrect.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            # Authentification par username
            username = username

        # CORRECTION: authenticate() ne prend pas 'email' comme paramètre
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active:
                return Response(
                    {'error': 'Votre compte est désactivé.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
                
            # Générer les tokens JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Création de la reponse
            response = Response({
               'user': {
                   'user':user.id,
                    'username': user.username,
                    'email':user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                'message':'Connexion Réussie.'
            }, status=status.HTTP_200_OK
            )

            # Définir les cookies HttpOnly
            # Access Token cookie (15 minutes ou 1 jour selon votre configuration)
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                max_age=24 * 60 * 60,  # 1 jour (votre settings)
            )

            # Refresh Token cookie (7 jours)
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                max_age=7 * 24 * 60 * 60,  # 7 jours
            )

            return response
        
        else:
            return Response(
                {'error': 'Email/Nom d\'utilisateur ou mot de passe incorrect.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
class CustomTokenRefreshView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Récupérer le refresh token depuis le cookie
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not refresh_token:
            return Response(
                {'error': 'Refresh token manquant. Veuillez vous reconnecter.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            # Valider et rafraîchir le token
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            
            # Créer la réponse
            response = Response({
                'message': 'Token rafraîchi avec succès.'
            }, status=status.HTTP_200_OK)
            
            # Mettre à jour le cookie access_token
            response.set_cookie(
                key='access_token',
                value=new_access_token,
                httponly=True,
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                max_age=24 * 60 * 60,  # 1 jour
            )
            
            # Si rotation des refresh tokens est activée
            if settings.SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS', False):
                # Blacklist l'ancien refresh token
                if settings.SIMPLE_JWT.get('BLACKLIST_AFTER_ROTATION', False):
                    try:
                        refresh.blacklist()
                    except AttributeError:
                        # Si blacklist n'est pas configuré
                        pass
                
                # Créer un nouveau refresh token
                user_id = refresh.payload.get('user_id')
                if user_id:
                    try:
                        user = CustomUser.objects.get(id=user_id)
                        new_refresh = RefreshToken.for_user(user)
                        
                        # Mettre à jour le cookie refresh_token
                        response.set_cookie(
                            key='refresh_token',
                            value=str(new_refresh),
                            httponly=True,
                            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                            max_age=7 * 24 * 60 * 60,  # 7 jours
                        )
                    except CustomUser.DoesNotExist:
                        pass
            
            return response
            
        except (TokenError, InvalidToken) as e:
            return Response(
                {'error': 'Token invalide ou expiré. Veuillez vous reconnecter.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

class LogoutView(APIView):
    
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