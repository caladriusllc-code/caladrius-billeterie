from django.urls import path
from .views import OrderCreateListView, OrderDetailView, PaymentWebhookView

urlpatterns = [
    # Gestion globale des commandes (Création & Liste)
    # POST /api/orders/ -> Créer une commande
    # GET /api/orders/  -> Liste des commandes
    path('orders/', OrderCreateListView.as_view(), name='order-list-create'),
    
    # Détail d'une commande spécifique
    # GET /api/orders/<uuid:pk>/
    path('orders/<uuid:pk>/', OrderDetailView.as_view(), name='order-detail'),
    
    # Validation du paiement et déclenchement de la génération de tickets
    # POST /api/orders/payment-confirm/
    path('orders/payment-confirm/', PaymentWebhookView.as_view(), name='payment-confirm'),
]