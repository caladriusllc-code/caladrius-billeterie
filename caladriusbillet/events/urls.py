from django.urls import path
from .views import (EventView, ManageEvent)

urlpatterns = [
    path('', EventView.as_view(), name='event-view'),
    path('manage-event/', ManageEvent.as_view(), name='manage-event')
]