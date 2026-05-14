from django.urls import path
from .views import home, CreateUserView, OrganisateurDashboardView, OrganisateurLoginView, OrganisateurLogoutView, OrganisateurRegisterView, CheckAuthStatusView


urlpatterns = [
    path('', home, name='home'),
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('organisateur/register/', OrganisateurRegisterView.as_view(), name='organisateur_register'),  # ✅ Changé: minuscule pour cohérence
    path('organisateur/login/', OrganisateurLoginView.as_view(), name='organisateur_login'),
    path('organisateur/dashboard/', OrganisateurDashboardView.as_view(), name='organisateur_dashboard'),  # ✅ Corrigé: dashboard
    path('organisateur/logout/', OrganisateurLogoutView.as_view(), name='organisateur_logout'),
    path('auth/status/', CheckAuthStatusView.as_view(), name='auth_status'), 
]