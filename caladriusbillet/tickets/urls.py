# tickets/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GuestViewSet, OrderViewSet, PublicEventViewSet

router = DefaultRouter()
router.register(r'guests', GuestViewSet, basename='guest')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'public/events', PublicEventViewSet, basename='public-events')

urlpatterns = [
    path('api/', include(router.urls)),
]

