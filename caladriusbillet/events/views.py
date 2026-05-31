from django.shortcuts import render
from .serializers import EventSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Event

class EventListView(APIView):
    """Espace public : Liste de tous les événements disponibles"""
    permission_classes = [AllowAny]

    def get(self, request):
        # 🧠 Optimisation : select_related charge l'organisateur et prefetch_related
        # charge tous les types de tickets en seulement 2 requêtes SQL au lieu de dizaines.
        events = Event.objects.select_related('organizer').prefetch_related('ticket_types').all()
        
        if not events.exists():
            return Response({
                'status': 'error',
                'message': 'Aucun événement disponible pour l\'instant.'
            }, status=status.HTTP_404_NOT_FOUND)
            
        # 💡 Ajout indispensable du contexte de la requête ici aussi
        serializer = EventSerializer(events, many=True, context={'request': request})
        return Response({
            'status': 'success',
            'events': serializer.data
        }, status=status.HTTP_200_OK)
    

class OrganizerDashboardView(APIView):
    """Espace Manager : Permet à l'organisateur de piloter son activité (Dashboard)"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Permet à l'organisateur de voir TOUS les événements qu'il a publiés, 
        ainsi que les statistiques de ventes de ses tickets (restants et vendus)"""
        # Optimisation SQL également pour le tableau de bord de l'organisateur
        my_events = Event.objects.filter(organizer=request.user).prefetch_related('ticket_types')
        
        if not my_events.exists():
            return Response({
                'status': 'success',
                'message': "Vous n'avez publié aucun événement pour le moment.",
                'total_published': 0,
                'my_events': []
            }, status=status.HTTP_200_OK)
            
        serializer = EventSerializer(my_events, many=True, context={'request': request})
        return Response({
            'status': 'success',
            'total_published': my_events.count(),
            'my_events': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """Permet à l'organisateur de créer un événement avec toutes ses caractéristiques 
        ET ses différentes catégories de tickets associés en même temps"""
        serializer = EventSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Le serializer s'occupe d'extraire request.user grâce au contexte transmis
            event = serializer.save()
            return Response({
                'status': 'success',
                'message': 'Votre événement et vos tickets ont été publiés avec succès !',
                'event': EventSerializer(event, context={'request': request}).data
            }, status=status.HTTP_201_CREATED)
            
        return Response({
            'status': 'error',
            'message': 'Erreur de validation des champs',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)