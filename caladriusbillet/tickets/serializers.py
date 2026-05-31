from rest_framework import serializers
from .models import Order, OrderItem, Ticket

class TicketSerializer(serializers.ModelSerializer):
    """Serializer pour afficher les détails d'un ticket individuel généré"""
    ticket_type_name = serializers.CharField(source='ticket_type.name', read_only=True)
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'ticket_number', 'ticket_type_name', 'status', 
            'attendee_name', 'attendee_email', 'price', 
            'seat_number', 'row_number', 'qr_code', 'created_at'
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer pour afficher ou saisir les lignes d'un panier/commande"""
    ticket_type_name = serializers.CharField(source='ticket_type.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['ticket_type', 'ticket_type_name', 'quantity', 'unit_price', 'subtotal']
        read_only_fields = ['unit_price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    generated_tickets = TicketSerializer(many=True, read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'user_email', 'event', 'event_title',
            'total_amount', 'status', 'payment_method', 'payment_id', 
            'paid_at', 'created_at', 'expires_at', 'items', 'generated_tickets'
        ]
        read_only_fields = ['id', 'order_number', 'user', 'total_amount', 'status']