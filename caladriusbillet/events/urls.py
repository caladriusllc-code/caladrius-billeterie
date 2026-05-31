from django.urls import path
from .views import EventListView, OrganizerDashboardView

urlpatterns = [
    # Route publique pour voir tous les événements
    path('', EventListView.as_view(), name='event-list'),
    
    # Route privée dashboard (Créer et voir MES événements + Ventes de tickets)
    path('dashboard/', OrganizerDashboardView.as_view(), name='organizer-dashboard'),
]