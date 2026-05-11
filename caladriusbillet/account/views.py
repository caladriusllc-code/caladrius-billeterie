from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CustomerClassSerializer
from django.utils.translation import gettext_lazy as _


# Create your views here.
def home(request):
    return HttpResponse("Hello, World!")

class CreateUserView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = CustomerClassSerializer(data=request.data)

        try:

            if serializer.is_valid():
                user = serializer.save()
                return Response(
                    {
                        "user": serializer.data,
                        'message': _("Votre compte a été créé avec succès.")
                    }, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {
                        "errors": serializer.errors,
                        'message': _("La création du compte a échoué. Veuillez vérifier les données fournies.")
                    }, status=status.HTTP_400_BAD_REQUEST
                )
        
        except Exception as e:
            return Response(
                {
                    "error": str(e),
                    'message': _("Une erreur inattendue s'est produite lors de la création du compte.")
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )