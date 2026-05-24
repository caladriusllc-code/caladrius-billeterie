from django.shortcuts import render
from .serializers import EventSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Event
# Create your views here.

class EventView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        
        events = Event.objects.all()

        if not events.exists():

            return Response(
                {
                    'message': 'Aucun évènement pour l\'instant',
                    'status': 'error',
                }, status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = EventSerializer(events, many=True)
        
        return Response(
            {
                'message': 'Evènements récupérées avec succès',
                'status': 'success',
                'events': serializer.data
            },
            status=status.HTTP_200_OK
        )

class ManageEvent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EventSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            event = serializer.save()
            return Response({
                'message': 'Nouvel événement ajouté',
                'status': 'succès',
                'event': EventSerializer(event).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Erreur de validation',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)   
        