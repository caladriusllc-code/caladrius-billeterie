from django.urls import path
from .views import BookTicketsView, ValidateTicketScanView

urlpatterns = [
    # Route client pour réserver / voir son historique
    path('buy/', BookTicketsView.as_view(), name='book-tickets'),
    
    # Route organisateur pour scanner le QR Code à l'entrée
    path('scan-validate/', ValidateTicketScanView.as_view(), name='validate-scan'),
]