from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import (
    CreateUserView, 
    CustomTokenRefreshView,
    LoginView,
    LogoutView     
)

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('login/', LoginView.as_view(), name='user_login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]