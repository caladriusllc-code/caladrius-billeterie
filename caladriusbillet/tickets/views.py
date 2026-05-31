from rest_framework import views, status
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from django.apps import apps

from .models import Order, OrderItem, Ticket
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated

class OrderCreateListView(views.APIView):
    permission_classes = [IsAuthenticated] # Optionnel : s'assurer qu'un utilisateur est connecté

    def post(self, request, *args, **kwargs):
        data = request.data
        items_data = data.get('items', [])

        if not items_data:
            return Response({"error": "Le panier ne peut pas être vide."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            serializer = OrderSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            
            # ✅ ON INJECTE L'USER CONNECTÉ ICI
            order = serializer.save(user=request.user)

            total_amount = 0
            TicketType = apps.get_model('events', 'TicketType')

            for item in items_data:
                try:
                    ticket_type = TicketType.objects.get(id=item['ticket_type'])
                except TicketType.DoesNotExist:
                    return Response({"error": "Type de ticket introuvable."}, status=status.HTTP_400_BAD_REQUEST)

                quantity = int(item['quantity'])
                unit_price = ticket_type.price
                
                order_item = OrderItem.objects.create(
                    order=order,
                    ticket_type=ticket_type,
                    quantity=quantity,
                    unit_price=unit_price
                )
                total_amount += order_item.subtotal

            order.total_amount = total_amount
            order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class OrderDetailView(views.APIView):
    """
    Vue pour récupérer une commande précise.
    """
    def get(self, request, pk, *args, **kwargs):
        """GET /api/orders/<id>/ -> Détails d'une commande (inclut les tickets si payée)"""
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Commande introuvable."}, status=status.HTTP_404_NOT_FOUND)


class PaymentWebhookView(views.APIView):
    """
    Vue appelée lors de la confirmation du paiement.
    """
    def post(self, request, *args, **kwargs):
        """POST /api/orders/payment-confirm/ -> Valide le paiement et génère les tickets"""
        order_id = request.data.get('order_id')
        payment_id = request.data.get('payment_id')         # Référence de la passerelle (Wave, Money...)
        payment_method = request.data.get('payment_method') # Ex: "Wave"

        try:
            order = Order.objects.get(id=order_id)
            
            if order.status == 'paid':
                return Response({"message": "Commande déjà traitée et payée."}, status=status.HTTP_200_OK)

            with transaction.atomic():
                # 1. Mise à jour du statut de la commande
                order.status = 'paid'
                order.payment_id = payment_id
                order.payment_method = payment_method
                order.paid_at = timezone.now()
                order.save()

                # 2. Éclatement des OrderItems en Tickets individuels uniques
                for item in order.items.all():
                    for _ in range(item.quantity):
                        Ticket.objects.create(
                            order=order,
                            event=order.event,
                            ticket_type=item.ticket_type,
                            price=item.unit_price,
                            attendee_name=order.guest.full_name,
                            attendee_email=order.guest.email,
                            attendee_phone=getattr(order.guest, 'phone', '')
                        )

            return Response({
                "message": "Paiement validé avec succès, tickets générés !",
                "order": OrderSerializer(order).data
            }, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({"error": "Commande introuvable."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)