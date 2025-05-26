from django.urls import path
from .views import *
from rest_framework.authtoken import views
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/login/',views.ObtainAuthToken.as_view(), name='token'),
    path('custom/token/login',CustomObtainToken.as_view(), name='custom-token'),


]

