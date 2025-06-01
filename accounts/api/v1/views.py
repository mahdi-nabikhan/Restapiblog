from django.conf import settings
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, UpdateAPIView, RetrieveUpdateAPIView
from .serializers import *
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.core.mail import send_mail
from django.template.loader import render_to_string
from accounts.api.v1.utils import *

class RegisterView(GenericAPIView):
    """
        RegisterView handles user registration.

        POST /accounts/api/v1/register/
        -------------------------------
        This endpoint allows a new user to register with email and password.

        Request data (JSON):
        {
            "email": "user@example.com",
            "password": "strong_password",
            "password2": "strong_password"
        }

        Response (201 Created):
        {
            "email": "user@example.com"
        }

        Response (400 Bad Request):
        {
            "password": ["This field is required."],
            "password2": ["Passwords do not match."]
        }
        """
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        """
                Handle POST request to register a new user.
                Validates the input data using UserRegistrationSerializer.
                On success, saves the user and returns serialized user data.
                On failure, returns validation errors.
        """
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomObtainToken(views.ObtainAuthToken):
    """
        CustomObtainToken generates an authentication token for a valid user.

        POST /accounts/api/v1/custom/token/login/
        ------------------------------------------
        This endpoint authenticates a user and returns an authentication token.

        Request data (JSON):
        {
            "email": "user@example.com",
            "password": "user_password"
        }

        Successful Response (200 OK):
        {
            "user_id": 1,
            "token": "c1b2f1e5cf3c40d292f49d...",
            "email": "user@example.com"
        }

        Error Response (400 Bad Request):
        {
            "non_field_errors": ["Unable to log in with provided credentials."]
        }
        """
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        """
                Handle POST request for user login and token generation.

                Validates the credentials using CustomAuthTokenSerializer.
                If valid, returns (or creates) a Token object and returns token info.
        """

        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, create = Token.objects.get_or_create(user=user)
            return Response({'user_id': user.pk, 'token': token.key, 'email': user.email})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomDiscardAuthToken(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenPairView(TokenObtainPairView):
    serializer_class = CustomObtainPairSerializer


class ChangePasswordView(UpdateAPIView):
    model = User
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old password': 'your password is wrong'}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response({'massage': 'password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)


class ProfileApiView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_queryset(self):
        obj = get_object_or_404(Profile, pk=self.request.user.pk)
        return obj


class SendEmailView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        send_mail(
            subject='Test Email',
            message='This is a test email from Django to smtp4dev.',
            from_email='test@example.com',
            recipient_list=['recipient@example.com'],
            fail_silently=False
        )
        return Response({'massage': 'email send successfully '})


def send_mail_with_template(template_name, context, from_email, recipient_list):
    subject = 'Your Subject'
    message = render_to_string(template_name, context)
    send_mail(subject, message, from_email, recipient_list)

class SendEmailApiView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        message= EmailMessage('email/hello.tpl',{'name':'mmd'},'asus@gmail.com',to=['mmd@gmail.com'])
        EmailThread(message).start()
        return Response({'message': 'email sent'})
