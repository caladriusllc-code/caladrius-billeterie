from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from .models import Order, Ticket
from .serializers import OrderSerializer

class BookTicketsView(APIView):
    """Permet aux acheteurs (Connectés OU Invités) de commander et de voir l'historique (connectés uniquement)"""
    
    def get_permissions(self):
        # Permettre à tout le monde (invités inclus) de faire un POST pour acheter
        if self.request.method == 'POST':
            return [AllowAny()]
        # Seuls les utilisateurs connectés peuvent faire un GET pour voir leur historique
        return [IsAuthenticated()]

    def get(self, request):
        """Récupère l'historique d'achat de l'utilisateur connecté"""
        my_orders = Order.objects.filter(user=request.user).prefetch_related(
            'items__tickets', 
            'items__ticket_type', 
            'event'
        )
        serializer = OrderSerializer(my_orders, many=True, context={'request': request})
        return Response({'status': 'success', 'my_orders': serializer.data}, status=status.HTTP_200_OK)
        
    def post(self, request):
        """Passer une commande de tickets (Achat connecté ou invité)"""
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response({
                'status': 'success',
                'message': 'Félicitations ! Vos billets et QR Codes ont été générés avec succès.',
                'order': OrderSerializer(order, context={'request': request}).data
            }, status=status.HTTP_201_CREATED)
            
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ValidateTicketScanView(APIView):
    """Espace Organisateur : Reçoit le code du QR code scanné pour valider l'accès"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        unique_code = request.data.get('unique_code')
        if not unique_code:
            return Response({
                'status': 'error', 
                'message': 'Le code unique du billet est manquant.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # On récupère le billet unique ainsi que l'événement lié
            ticket = Ticket.objects.select_related('order_item__ticket_type__event').get(unique_code=unique_code)
            event = ticket.order_item.ticket_type.event
            
            # Sécurité : Seul l'organisateur de cet événement précis a le droit de valider le scan
            if event.organizer != request.user:
                return Response({
                    'status': 'error', 
                    'message': "Accès refusé. Vous n'êtes pas l'organisateur de cet événement."
                }, status=status.HTTP_403_FORBIDDEN)
                
            # Anti-fraude : Le billet a-t-il déjà servi ?
            if ticket.is_scanned:
                # ✅ CORRECTION : Utilisation de localtime pour afficher l'heure correcte selon la configuration Django
                local_scanned_at = timezone.localtime(ticket.scanned_at)
                return Response({
                    'status': 'fraud',
                    'message': f'🚨 FRAUDE DÉTECTÉE : Ce ticket a déjà été scanné le {local_scanned_at.strftime("%d/%m/%Y à %H:%M")}. Entrée refusée !'
                }, status=status.HTTP_200_OK)

            # Si tout est en ordre : On valide le passage
            ticket.is_scanned = True
            ticket.scanned_at = timezone.now()
            ticket.save()

            return Response({
                'status': 'success',
                'message': f'✅ TICKET VALIDE. Porteur : {ticket.holder_name}. Catégorie : {ticket.order_item.ticket_type.name}. Laissez passer !',
                'event_title': event.title
            }, status=status.HTTP_200_OK)

        except Ticket.DoesNotExist:
            return Response({
                'status': 'error', 
                'message': "❌ TICKET INCONNU. Ce billet n'existe pas dans le système."
            }, status=status.HTTP_404_NOT_FOUND)