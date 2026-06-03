from rest_framework import serializers
from django.db import transaction
from .models import Order, OrderItem, Ticket
from events.models import TicketType

class OrderItemInputSerializer(serializers.Serializer):
    """Permet de recevoir un article du panier (ex: TicketType X avec quantité Y)"""
    ticket_type_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)
    holder_name = serializers.CharField(max_length=200, required=False, allow_blank=True)

class TicketDetailSerializer(serializers.ModelSerializer):
    """Affiche les détails d'un billet généré"""
    ticket_type_name = serializers.CharField(source='order_item.ticket_type.name', read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'ticket_type_name', 'holder_name', 'unique_code', 'qr_code_image', 'is_scanned']

class OrderItemDetailSerializer(serializers.ModelSerializer):
    """Affiche le détail d'une ligne de commande avec ses tickets associés"""
    ticket_type_name = serializers.CharField(source='ticket_type.name', read_only=True)
    tickets = TicketDetailSerializer(many=True, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'ticket_type_name', 'quantity', 'unit_price', 'subtotal', 'tickets']

class OrderSerializer(serializers.ModelSerializer):
    buyer_email = serializers.SerializerMethodField()
    event_title = serializers.CharField(source='event.title', read_only=True)
    items = OrderItemDetailSerializer(many=True, read_only=True)
    cart_items = OrderItemInputSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'buyer_email', 'guest_email', 'guest_name', 
            'event_title', 'total_amount', 'status', 'created_at', 'items', 'cart_items'
        ]
        read_only_fields = ['id', 'order_number', 'total_amount', 'status', 'created_at']

    def get_buyer_email(self, obj):
        return obj.user.email if obj.user else obj.guest_email

    def validate(self, attrs):
        request = self.context.get('request')
        
        # 1. Protection au cas où le contexte de la requête est absent (ex: tests unitaires ou scripts)
        if not request:
            return attrs
            
        user = request.user
        
        # 2. Sécurité : Vérification correcte d'un utilisateur anonyme / non connecté
        if not user or user.is_anonymous:
            guest_email = attrs.get('guest_email')
            guest_name = attrs.get('guest_name')
            
            if not guest_email or not guest_name:
                raise serializers.ValidationError({
                    "error": "Pour un achat invité, vous devez fournir un nom ('guest_name') et un email ('guest_email')."
                })
        return attrs

    def create(self, validated_data):
        cart_items_data = validated_data.pop('cart_items')
        guest_email = validated_data.get('guest_email', None)
        guest_name = validated_data.get('guest_name', None)
        
        request = self.context.get('request')
        
        # 3. Récupération sécurisée du statut d'authentification
        user = None
        if request and request.user and request.user.is_authenticated:
            user = request.user

        # L'utilisation de transaction.atomic garantit que si une seule étape plante, rien n'est écrit
        with transaction.atomic():
            try:
                first_ticket_type = TicketType.objects.get(id=cart_items_data[0]['ticket_type_id'])
                event = first_ticket_type.event
            except (IndexError, TicketType.DoesNotExist):
                raise serializers.ValidationError({"error": "Le panier est vide ou invalide."})

            # Création de la commande initiale
            order = Order.objects.create(
                user=user, 
                guest_email=guest_email,
                guest_name=guest_name,
                event=event, 
                status='paid', 
                total_amount=0
            )
            total_amount = 0

            for item in cart_items_data:
                try:
                    ticket_type = TicketType.objects.select_for_update().get(id=item['ticket_type_id'])
                except TicketType.DoesNotExist:
                    raise serializers.ValidationError({"error": f"Le type de ticket {item['ticket_type_id']} n'existe pas."})
                
                quantity = item['quantity']
                holder = item.get('holder_name', '')

                # 4. Vérification de la limite imposée par le TicketType (max_per_order)
                if hasattr(ticket_type, 'max_per_order') and quantity > ticket_type.max_per_order:
                    raise serializers.ValidationError({
                        "error": f"Vous ne pouvez pas prendre plus de {ticket_type.max_per_order} tickets pour la catégorie '{ticket_type.name}'."
                    })

                if ticket_type.quantity_available < quantity:
                    raise serializers.ValidationError({"error": f"Stock insuffisant pour '{ticket_type.name}'."})

                # Soustraction des stocks
                ticket_type.quantity_available -= quantity
                ticket_type.save()

                subtotal = ticket_type.price * quantity
                total_amount += subtotal

                # Création de la ligne de commande
                order_item = OrderItem.objects.create(
                    order=order, ticket_type=ticket_type, quantity=quantity, unit_price=ticket_type.price
                )

                # Génération des billets unitaires
                for _ in range(quantity):
                    # 5. Fallback du nom du porteur de ticket
                    if holder:
                        final_holder_name = holder
                    elif user:
                        final_holder_name = getattr(user, 'username', user.email)
                    else:
                        final_holder_name = guest_name

                    Ticket.objects.create(
                        order_item=order_item,
                        holder_name=final_holder_name
                    )

            # Mise à jour finale du montant global de la commande
            order.total_amount = total_amount
            order.save()

        # 💡 DÉCLENCHEMENT DE L'EMAIL (Hors de la transaction pour des raisons de performance)
        try:
            from .emails import send_ticket_email
            send_ticket_email(order)
        except Exception as e:
            # On log l'erreur pour ne pas faire planter l'achat de l'utilisateur si le serveur d'e-mail a un problème
            print(f"Erreur d'envoi d'email lors de la commande {order.order_number}: {str(e)}")

        return order