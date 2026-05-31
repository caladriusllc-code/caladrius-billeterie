from rest_framework import serializers
from .models import Event, TicketType
from account.serializers import CustomerClassSerializer

class TicketTypeSerializer(serializers.ModelSerializer):
    # Les tickets vendus sont calculés automatiquement en lecture seule par le modèle
    tickets_sold = serializers.IntegerField(read_only=True)

    class Meta:
        model = TicketType
        fields = [
            'id', 'name', 'description', 'price', 
            'quantity_initial', 'quantity_available', 
            'max_per_order', 'is_active', 'tickets_sold'
        ]
        # 💡 AJOUTE CETTE LIGNE CI-DESSOUS :
        read_only_fields = ['id', 'quantity_available', 'tickets_sold']

        

class EventSerializer(serializers.ModelSerializer):
    # 1. Utilise CustomerClassSerializer pour afficher les détails de l'organisateur en GET
    organizer = CustomerClassSerializer(read_only=True)
    organizer_name = serializers.CharField(source='organizer.username', read_only=True)
    
    # 2. Permet d'envoyer ou de recevoir une liste de tickets imbriqués. 
    # required=False évite les bugs si l'organisateur ne crée aucun ticket au départ.
    ticket_types = TicketTypeSerializer(many=True, required=False)
    
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['id', 'organizer', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        Extrait les tickets du JSON, crée l'événement en lui attachant request.user,
        puis génère automatiquement les TicketTypes liés.
        """
        ticket_types_data = validated_data.pop('ticket_types', [])
        
        # Récupération de l'utilisateur connecté via le contexte de la vue
        request = self.context.get('request')
        event = Event.objects.create(organizer=request.user, **validated_data)
        
        # Création automatique de chaque type de ticket lié à cet événement
        for ticket_type_data in ticket_types_data:
            qty_initial = ticket_type_data.get('quantity_initial', 0)
            TicketType.objects.create(
                event=event, 
                quantity_available=qty_initial, # Au départ, ce qui reste = stock de départ
                **ticket_type_data
            )
            
        return event

    def validate(self, attrs):
        """
        Validation logique des dates en amont pour renvoyer des réponses 
        propres et ciblées sous forme d'erreurs d'API (Statut 400).
        """
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        sales_start_date = attrs.get('sales_start_date')
        sales_end_date = attrs.get('sales_end_date')

        errors = {}
        if start_date and end_date and end_date <= start_date:
            errors['end_date'] = "La date de fin doit être postérieure à la date de début."
            
        if sales_start_date and sales_end_date and sales_end_date <= sales_start_date:
            errors['sales_end_date'] = "La date de fin des ventes doit être postérieure à la date de début des ventes."
            
        if sales_start_date and start_date and sales_start_date >= start_date:
            errors['sales_start_date'] = "Le début des ventes doit avoir lieu avant le début de l'évènement."

        if errors:
            raise serializers.ValidationError(errors)
            
        return attrs