# tickets/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Ticket
from .serializers import TicketSerializer
from events.models import Event, TicketType


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def create_ticket(self, request):
        """
        Créer un ticket simple
        """
        event_id = request.data.get('event_id')
        ticket_type_id = request.data.get('ticket_type_id')
        attendee_name = request.data.get('attendee_name')
        attendee_email = request.data.get('attendee_email')
        quantity = request.data.get('quantity', 1)
        
        # Vérifications
        try:
            event = Event.objects.get(id=event_id)
            ticket_type = TicketType.objects.get(id=ticket_type_id)
        except (Event.DoesNotExist, TicketType.DoesNotExist):
            return Response({'error': 'Événement ou type de ticket non trouvé'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        # Créer le ticket
        ticket = Ticket.objects.create(
            event=event,
            ticket_type=ticket_type,
            buyer=request.user,
            attendee_name=attendee_name,
            attendee_email=attendee_email,
            price=ticket_type.price,
            quantity=quantity
        )
        
        return Response({
            'success': True,
            'message': 'Ticket créé avec succès',
            'ticket': TicketSerializer(ticket).data
        }, status=status.HTTP_201_CREATED)