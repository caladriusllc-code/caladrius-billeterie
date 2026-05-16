from django.urls import path
from .views import (
    home, 
    CreateUserView, 
    OrganisateurDashboardView, 
    OrganisateurLoginView, 
    OrganisateurLogoutView, 
    OrganisateurRegisterView, 
    CheckAuthStatusView,
    UtilisateurRegisterView,    
    UtilisateurLoginView,         
    UtilisateurProfileView        
)

urlpatterns = [
    path('', home, name='home'),
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('organisateur/register/', OrganisateurRegisterView.as_view(), name='organisateur_register'),
    path('organisateur/login/', OrganisateurLoginView.as_view(), name='organisateur_login'),
    path('organisateur/dashboard/', OrganisateurDashboardView.as_view(), name='organisateur_dashboard'),
    path('organisateur/logout/', OrganisateurLogoutView.as_view(), name='organisateur_logout'),
    path('auth/status/', CheckAuthStatusView.as_view(), name='auth_status'), 
    path('utilisateur/register/', UtilisateurRegisterView.as_view(), name='utilisateur_register'), 
    path('utilisateur/login/', UtilisateurLoginView.as_view(), name='utilisateur_login'),          
    path('utilisateur/profile/', UtilisateurProfileView.as_view(), name='utilisateur_profile'),    
]