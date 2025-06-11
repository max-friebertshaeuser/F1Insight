from django.urls import path
from .views import RegisterView, profile_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'user_auth'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', profile_view, name='profile'),
]