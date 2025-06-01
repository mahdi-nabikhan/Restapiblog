import jwt
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
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class SendTokenActivationRegisterView(GenericAPIView):
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
            user = get_object_or_404(User, email=serializer.validated_data['email'])

            # Generate JWT tokens for the user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Prepare email message content
            message_body = f"""
                    Hello {user.email},

                    Here is your JWT access token:
                    {access_token}

                    If you did not request this, please ignore this email.
                    """

            # Send the email
            email_message = EmailMessage('email/activation_email.tpl',
                                         subject="Your Access Token",
                                         from_email="noreply@example.com",
                                         to=[serializer.validated_data['email']],
                                         context={'token': refresh}
                                         )
            email_message.send()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    """
    SendEmailApiView sends a JWT access token to a user's email address.

    GET /accounts/api/v1/send-email/
    --------------------------------
    This endpoint is used to generate a JWT token for a specific user
    (based on hardcoded email for testing), and sends the access token via email.

    Usage:
        - This is typically used in development/testing environments.
        - The email is hardcoded as 'mmd@gmail.com'.

    Response:
        {
            "message": "Token sent via email"
        }

    Errors:
        - 404 if the user with given email does not exist.
    """

    def get(self, request, *args, **kwargs):
        # Define the target email address
        email = 'mmd@gmail.com'

        # Fetch user object by email
        user = get_object_or_404(User, email=email)

        # Generate JWT tokens for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Prepare email message content
        message_body = f"""
        Hello {user.email},

        Here is your JWT access token:
        {access_token}

        If you did not request this, please ignore this email.
        """

        # Send the email
        email_message = EmailMessage('email/hello.tpl',
                                     subject="Your Access Token",
                                     body=message_body,
                                     from_email="noreply@example.com",
                                     to=[email],
                                     context={'token': refresh}
                                     )
        email_message.send()

        return Response({'message': 'Token sent via email'}, status=status.HTTP_200_OK)

    def get_tokens_for_user(self, user):
        """
        Generate and return both refresh and access tokens for a given user.
        """
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class ActivationApiView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = token.get('user_id')
        except jwt.ExpiredSignatureError:
            return Response(data={'detail': 'token has been expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response(data={'detail': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(pk=user_id)
        user.is_verified = True
        if user.is_verified:
            return Response({'detail': 'your account has been activated'})
        user.save()
        return Response(data={'detail': 'user has been activated'}, status=status.HTTP_200_OK)


class ActivationResendApiView(APIView):
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Prepare email message content
            message_body = f"""
                               Hello {user},

                               Here is your JWT access token:
                               {access_token}

                               If you did not request this, please ignore this email.
                               """

            # Send the email
            email_message = EmailMessage('email/activation_email.tpl',
                                         subject="Your Access Token",
                                         from_email="noreply@example.com",
                                         to=[serializer.validated_data.get('email')],
                                         context={'token': refresh}
                                         )
            email_message.send()
            return Response({'message': 'Token resent to your email'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'detail': 'email is empty'}, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        """
        Generate and return both refresh and access tokens for a given user.
        """
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
