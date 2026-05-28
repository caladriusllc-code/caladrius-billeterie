# tickets/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from .models import Guest, Ticket, Order, OrderItem
from .serializers import (
    GuestSerializer, TicketSerializer, OrderSerializer,
    OrderCreateSerializer, OrderPaymentSerializer, 
    GuestOrderSerializer, MyTicketsSerializer
)
from events.models import Event, TicketType


class GuestViewSet(viewsets.ModelViewSet):
    """Gestion des invités"""
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def create_or_get(self, request):
        """Créer ou récupérer un guest par email"""
        email = request.data.get('email')
        
        if not email:
            return Response({'error': 'Email requis'}, status=status.HTTP_400_BAD_REQUEST)
        
        guest, created = Guest.objects.get_or_create(
            email=email,
            defaults={
                'first_name': request.data.get('first_name', ''),
                'last_name': request.data.get('last_name', ''),
                'phone': request.data.get('phone', ''),
            }
        )
        
        serializer = GuestSerializer(guest)
        return Response({
            'success': True,
            'is_new': created,
            'guest': serializer.data
        })
    
    @action(detail=False, methods=['post'])
    def get_by_email(self, request):
        """Récupérer un guest par email"""
        email = request.data.get('email')
        
        if not email:
            return Response({'error': 'Email requis'}, status=status.HTTP_400_BAD_REQUEST)
        
        guest = Guest.objects.filter(email=email).first()
        
        if not guest:
            return Response({'error': 'Aucun guest trouvé'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GuestSerializer(guest)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    """Gestion des commandes"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def create_order(self, request):
        """
        ÉTAPE 1 & 2 : Créer une commande
        Client choisit événement + types de tickets
        """
        serializer = OrderCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        event_id = data['event_id']
        items_data = data['items']
        guest_data = data['guest']
        
        # Récupérer l'événement
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Événement non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        
        # Vérifier que l'événement est publié
        if not event.is_published:
            return Response({'error': 'Cet événement n\'est pas encore disponible'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Vérifier que la vente est ouverte
        now = timezone.now()
        if now < event.sale_start_date:
            return Response({'error': f'Ventes ouvertes à partir du {event.sale_start_date}'}, status=status.HTTP_400_BAD_REQUEST)
        if now > event.sale_end_date:
            return Response({'error': 'Ventes terminées pour cet événement'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Créer ou récupérer le guest
        guest, guest_created = Guest.objects.get_or_create(
            email=guest_data['email'],
            defaults={
                'first_name': guest_data.get('first_name', ''),
                'last_name': guest_data.get('last_name', ''),
                'phone': guest_data.get('phone', ''),
                'address': guest_data.get('address', ''),
                'city': guest_data.get('city', ''),
                'postal_code': guest_data.get('postal_code', ''),
                'country': guest_data.get('country', 'France'),
            }
        )
        
        # Créer la commande
        order = Order.objects.create(
            guest=guest,
            event=event,
            status='pending',
            expires_at=timezone.now() + timedelta(minutes=30)  # Expire dans 30 min
        )
        
        total_amount = Decimal('0.00')
        items_errors = []
        
        # Ajouter les items à la commande
        for item in items_data:
            ticket_type_id = item.get('ticket_type_id')
            quantity = item.get('quantity', 1)
            
            try:
                ticket_type = TicketType.objects.get(id=ticket_type_id, event=event)
            except TicketType.DoesNotExist:
                items_errors.append(f'Type de ticket {ticket_type_id} non trouvé')
                continue
            
            # Vérifier la disponibilité
            if ticket_type.quantity_available < quantity:
                items_errors.append(f'Plus que {ticket_type.quantity_available} tickets de type {ticket_type.name} disponibles')
                continue
            
            # Vérifier la limite par commande
            if quantity > ticket_type.max_per_order:
                items_errors.append(f'Maximum {ticket_type.max_per_order} tickets de type {ticket_type.name} par commande')
                continue
            
            # Créer l'item
            OrderItem.objects.create(
                order=order,
                ticket_type=ticket_type,
                quantity=quantity,
                unit_price=ticket_type.price
            )
            
            total_amount += ticket_type.price * quantity
        
        # Si des erreurs, supprimer la commande
        if items_errors:
            order.delete()
            return Response({'errors': items_errors}, status=status.HTTP_400_BAD_REQUEST)
        
        # Mettre à jour le montant total
        order.total_amount = total_amount
        order.save()
        
        # Retourner la réponse
        order_serializer = OrderSerializer(order)
        
        return Response({
            'success': True,
            'message': 'Commande créée avec succès',
            'is_new_guest': guest_created,
            'order': order_serializer.data,
            'payment_required': float(total_amount),
            'expires_in_minutes': 30
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def process_payment(self, request, pk=None):
        """
        ÉTAPE 3 : Traiter le paiement
        """
        order = self.get_object()
        
        # Vérifier que la commande est en attente
        if order.status != 'pending':
            return Response({'error': f'Commande déjà {order.status}'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Vérifier que la commande n'a pas expiré
        if order.expires_at and order.expires_at < timezone.now():
            order.status = 'expired'
            order.save()
            return Response({'error': 'Commande expirée. Veuillez recommencer.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Valider les données de paiement
        payment_serializer = OrderPaymentSerializer(data=request.data)
        if not payment_serializer.is_valid():
            return Response({'errors': payment_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        payment_data = payment_serializer.validated_data
        payment_method = payment_data['payment_method']
        payment_id = payment_data.get('payment_id', f"SIM_{order.order_number}")
        
        # ICI : Intégration avec Stripe, PayPal, etc.
        # Pour l'exemple, on simule un paiement réussi
        payment_success = True
        
        if not payment_success:
            return Response({
                'success': False,
                'error': 'Paiement échoué. Veuillez réessayer.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Mettre à jour la commande
        order.status = 'paid'
        order.payment_method = payment_method
        order.payment_id = payment_id
        order.paid_at = timezone.now()
        order.save()
        
        # Créer les tickets après paiement réussi
        tickets_created = []
        tickets_errors = []
        
        for item in order.items.all():
            ticket_type = item.ticket_type
            
            # Vérifier à nouveau la disponibilité (au cas où)
            if ticket_type.quantity_available < item.quantity:
                tickets_errors.append(f'Plus de tickets disponibles pour {ticket_type.name}')
                continue
            
            # Réduire la quantité disponible
            ticket_type.quantity_available -= item.quantity
            ticket_type.save()
            
            # Créer les tickets
            for i in range(item.quantity):
                ticket = Ticket.objects.create(
                    event=order.event,
                    ticket_type=ticket_type,
                    guest=order.guest,
                    attendee_name=order.guest.full_name,
                    attendee_email=order.guest.email,
                    attendee_phone=order.guest.phone,
                    price=item.unit_price,
                    quantity=1,
                    seat_number=item.ticket_type.seat_number if hasattr(item.ticket_type, 'seat_number') else '',
                    row_number=item.ticket_type.row_number if hasattr(item.ticket_type, 'row_number') else ''
                )
                tickets_created.append(ticket)
        
        # Si erreurs de tickets, annuler la commande et rembourser
        if tickets_errors:
            order.status = 'cancelled'
            order.save()
            return Response({
                'success': False,
                'errors': tickets_errors,
                'message': 'Problème lors de la création des tickets. Commande annulée.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Mettre à jour la date du dernier achat du guest
        order.guest.last_purchase_at = timezone.now()
        order.guest.save()
        
        # Sérialiser les tickets
        tickets_serializer = TicketSerializer(tickets_created, many=True)
        
        return Response({
            'success': True,
            'message': 'Paiement effectué avec succès',
            'order': OrderSerializer(order).data,
            'tickets': tickets_serializer.data,
            'tickets_count': len(tickets_created)
        })
    
    @action(detail=True, methods=['get'])
    def payment_status(self, request, pk=None):
        """Vérifier le statut du paiement"""
        order = self.get_object()
        
        return Response({
            'order_number': order.order_number,
            'status': order.status,
            'total_amount': float(order.total_amount),
            'is_paid': order.status == 'paid',
            'expires_at': order.expires_at,
            'paid_at': order.paid_at
        })
    
    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        """Annuler une commande (uniquement si non payée)"""
        order = self.get_object()
        
        if order.status == 'paid':
            return Response({'error': 'Impossible d\'annuler une commande déjà payée'}, status=status.HTTP_400_BAD_REQUEST)
        
        if order.status == 'cancelled':
            return Response({'error': 'Commande déjà annulée'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'cancelled'
        order.save()
        
        return Response({
            'success': True,
            'message': 'Commande annulée avec succès',
            'order_number': order.order_number
        })
    
    @action(detail=False, methods=['post'])
    def my_orders(self, request):
        """Récupérer les commandes d'un client par email"""
        serializer = GuestOrderSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        guest = Guest.objects.filter(email=email).first()
        
        if not guest:
            return Response({'error': 'Aucune commande trouvée pour cet email'}, status=status.HTTP_404_NOT_FOUND)
        
        orders = Order.objects.filter(guest=guest).order_by('-created_at')
        orders_serializer = OrderSerializer(orders, many=True)
        
        # Statistiques
        total_spent = orders.filter(status='paid').aggregate(total=models.Sum('total_amount'))['total'] or 0
        
        return Response({
            'guest': {
                'name': guest.full_name,
                'email': guest.email,
                'phone': guest.phone
            },
            'stats': {
                'total_orders': orders.count(),
                'paid_orders': orders.filter(status='paid').count(),
                'pending_orders': orders.filter(status='pending').count(),
                'total_spent': float(total_spent)
            },
            'orders': orders_serializer.data
        })
    
    @action(detail=False, methods=['post'])
    def my_tickets(self, request):
        """Récupérer tous les tickets d'un client par email"""
        email = request.data.get('email')
        
        if not email:
            return Response({'error': 'Email requis'}, status=status.HTTP_400_BAD_REQUEST)
        
        guest = Guest.objects.filter(email=email).first()
        
        if not guest:
            return Response({'error': 'Aucun ticket trouvé pour cet email'}, status=status.HTTP_404_NOT_FOUND)
        
        tickets = Ticket.objects.filter(guest=guest).select_related('event', 'ticket_type').order_by('-created_at')
        
        # Grouper par événement
        tickets_by_event = {}
        for ticket in tickets:
            event_name = ticket.event.title
            if event_name not in tickets_by_event:
                tickets_by_event[event_name] = {
                    'event_id': str(ticket.event.id),
                    'event_title': ticket.event.title,
                    'event_date': ticket.event.start_date,
                    'event_location': ticket.event.location,
                    'tickets': []
                }
            tickets_by_event[event_name]['tickets'].append(TicketSerializer(ticket).data)
        
        tickets_serializer = TicketSerializer(tickets, many=True)
        
        return Response({
            'guest': {
                'name': guest.full_name,
                'email': guest.email,
                'phone': guest.phone
            },
            'total_tickets': tickets.count(),
            'tickets_by_event': list(tickets_by_event.values()),
            'all_tickets': tickets_serializer.data
        })


class PublicEventViewSet(viewsets.ViewSet):
    """Vues publiques pour les événements"""
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def upcoming_events(self, request):
        """Récupérer les événements à venir"""
        now = timezone.now()
        
        events = Event.objects.filter(
            start_date__gt=now,
            is_published=True
        ).order_by('start_date')
        
        result = []
        for event in events:
            # Récupérer les types de tickets disponibles
            ticket_types = event.ticket_types.filter(
                is_active=True,
                quantity_available__gt=0
            )
            
            if ticket_types.exists():
                from events.serializers import EventSerializer
                result.append({
                    'event': EventSerializer(event).data,
                    'available_tickets': TicketTypePublicSerializer(ticket_types, many=True).data
                })
        
        return Response({
            'total_events': len(result),
            'events': result
        })
    
    @action(detail=True, methods=['get'])
    def event_detail(self, request, pk=None):
        """Détail d'un événement avec ses tickets"""
        from events.serializers import EventSerializer
        
        event = get_object_or_404(Event, id=pk, is_published=True)
        ticket_types = event.ticket_types.filter(is_active=True, quantity_available__gt=0)
        
        from .serializers import TicketTypePublicSerializer
        return Response({
            'event': EventSerializer(event).data,
            'available_tickets': TicketTypePublicSerializer(ticket_types, many=True).data
        })


# Importer à la fin pour éviter les imports circulaires
from django.db import models
from .serializers import TicketTypePublicSerializer