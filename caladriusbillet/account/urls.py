from django.urls import path
from .views import home, CreateUserView

urlpatterns = [
    path('', home, name='home'),
    path('create/', CreateUserView.as_view(), name='create_user')
]