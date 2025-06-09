from django.urls import path
from .views import *
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'api-v1'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/register/',SendTokenActivationRegisterView.as_view(), name='token-register'),
    path('token/login/', views.ObtainAuthToken.as_view(), name='token'),
    path('custom/token/login', CustomObtainToken.as_view(), name='custom-token'),
    path('discard/token/', CustomDiscardAuthToken.as_view(), name='discard-token'),
    path('jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
    path('jwt/custom/', CustomTokenPairView.as_view(), name='jwt-custom'),
    path('change/password', ChangePasswordView.as_view(), name='change-password'),
    path('profile/', ProfileApiView.as_view(), name='profile'),
    path('send/email/', SendEmailView.as_view(), name='send-email'),
    path('send/email/template/', SendEmailApiView.as_view(), name='send_templated_email'),
    path('activation/confirm/<str:token>/', ActivationApiView.as_view(), name='activation-confirm'),

]
