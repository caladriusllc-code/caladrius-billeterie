# tickets/serializers.py
from rest_framework import serializers
from .models import Guest, Ticket, Order, OrderItem
from events.models import Event, TicketType  


class GuestSerializer(serializers.ModelSerializer):
    """Serializer pour les invités"""
    full_name = serializers.CharField(read_only=True)
    total_purchases = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Guest
        fields = [
            'id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone',
            'address',
            'city',
            'postal_code',
            'country',
            'is_active',
            'total_purchases',
            'created_at',
            'updated_at',
            'last_purchase_at',
            'notes',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_purchase_at', 'total_purchases']


class TicketSerializer(serializers.ModelSerializer):
    """Serializer pour les tickets"""
    event_title = serializers.CharField(source='event.title', read_only=True)
    event_date = serializers.DateTimeField(source='event.start_date', read_only=True)
    event_location = serializers.CharField(source='event.location', read_only=True)
    organizer_name = serializers.CharField(source='event.organizer.username', read_only=True)
    ticket_type_name = serializers.CharField(source='ticket_type.name', read_only=True)
    guest_name = serializers.CharField(source='guest.full_name', read_only=True)
    purchaser_name = serializers.CharField(read_only=True)
    purchaser_email = serializers.EmailField(read_only=True)
    
    class Meta:
        model = Ticket
        fields = [
            'id',
            'ticket_number',
            'qr_code',
            'event',
            'event_title',
            'event_date',
            'event_location',
            'organizer_name',
            'ticket_type',
            'ticket_type_name',
            'guest',
            'guest_name',
            'attendee_name',
            'attendee_email',
            'attendee_phone',
            'price',
            'quantity',
            'seat_number',
            'row_number',
            'purchaser_name',
            'purchaser_email',
            'created_at',
        ]
        read_only_fields = ['id', 'ticket_number', 'qr_code', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer pour les lignes de commande"""
    ticket_type_name = serializers.CharField(source='ticket_type.name', read_only=True)
    ticket_type_price = serializers.DecimalField(source='ticket_type.price', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'ticket_type',
            'ticket_type_name',
            'ticket_type_price',
            'quantity',
            'unit_price',
            'subtotal',
        ]
        read_only_fields = ['id', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer pour les commandes (lecture seule)"""
    items = OrderItemSerializer(many=True, read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    event_date = serializers.DateTimeField(source='event.start_date', read_only=True)
    guest_name = serializers.CharField(source='guest.full_name', read_only=True)
    guest_email = serializers.EmailField(source='guest.email', read_only=True)
    total_tickets = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'guest',
            'guest_name',
            'guest_email',
            'event',
            'event_title',
            'event_date',
            'total_amount',
            'total_tickets',
            'status',
            'payment_method',
            'payment_id',
            'items',
            'created_at',
            'expires_at',
            'paid_at',
        ]
        read_only_fields = ['id', 'order_number', 'created_at', 'paid_at']


class OrderCreateSerializer(serializers.Serializer):
    """Serializer pour la création d'une commande"""
    event_id = serializers.UUIDField(required=True)
    items = serializers.ListField(
        child=serializers.DictField(),
        required=True,
        min_length=1
    )
    guest = serializers.DictField(required=True)
    
    def validate_event_id(self, value):
        """Vérifier que l'événement existe"""
        try:
            event = Event.objects.get(id=value)
            return value
        except Event.DoesNotExist:
            raise serializers.ValidationError("Événement non trouvé")
    
    def validate_items(self, value):
        """Vérifier les items de la commande"""
        if not value:
            raise serializers.ValidationError("Au moins un ticket requis")
        
        for item in value:
            if 'ticket_type_id' not in item:
                raise serializers.ValidationError("ticket_type_id requis pour chaque item")
            if 'quantity' not in item:
                raise serializers.ValidationError("quantity requise pour chaque item")
            
            quantity = item.get('quantity', 0)
            if quantity <= 0:
                raise serializers.ValidationError("La quantité doit être supérieure à 0")
        
        return value
    
    def validate_guest(self, value):
        """Vérifier les informations du guest"""
        required_fields = ['first_name', 'last_name', 'email', 'phone']
        for field in required_fields:
            if field not in value or not value[field]:
                raise serializers.ValidationError(f"{field} est requis")
        
        return value


class OrderPaymentSerializer(serializers.Serializer):
    """Serializer pour le paiement d'une commande"""
    payment_method = serializers.CharField(required=True, max_length=50)
    payment_id = serializers.CharField(required=False, allow_blank=True)
    
    def validate_payment_method(self, value):
        valid_methods = ['card', 'paypal', 'stripe', 'mobile_money']
        if value not in valid_methods:
            raise serializers.ValidationError(f"Méthode de paiement invalide. Choisir parmi: {valid_methods}")
        return value


class GuestOrderSerializer(serializers.Serializer):
    """Serializer pour récupérer les commandes d'un guest"""
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        guest = Guest.objects.filter(email=value).first()
        if not guest:
            raise serializers.ValidationError("Aucun guest trouvé avec cet email")
        return value


# ✅ CORRECTION 1 : TicketTypePublicSerializer avant EventPublicSerializer
class TicketTypePublicSerializer(serializers.ModelSerializer):
    """Serializer public pour les types de tickets"""
    class Meta:
        model = TicketType  # ✅ Plus d'import à l'intérieur
        fields = [
            'id',
            'name',
            'description',
            'price',
            'quantity_available',
            'max_per_order',
        ]


# ✅ CORRECTION 2 : EventPublicSerializer après TicketTypePublicSerializer
class EventPublicSerializer(serializers.Serializer):
    """Serializer public pour les événements avec leurs tickets"""
    id = serializers.UUIDField()
    title = serializers.CharField()
    description = serializers.CharField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    location = serializers.CharField()
    city = serializers.CharField()
    image = serializers.ImageField()
    organizer_name = serializers.CharField()
    available_tickets = TicketTypePublicSerializer(many=True)  # ✅ Maintenant disponible


class MyTicketsSerializer(serializers.Serializer):
    """Serializer pour la réponse des tickets d'un guest"""
    email = serializers.EmailField()
    total_tickets = serializers.IntegerField()
    tickets = TicketSerializer(many=True)