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
        SendTokenActivationRegisterView handles user registration with email verification via a JWT token.

        This endpoint registers a new user and sends a JWT access token to their email for account activation.

        POST /accounts/api/v1/register/send-token/
        ------------------------------------------

        ### Request Body (JSON)
        {
            "email": "user@example.com",
            "password": "strong_password",
            "password2": "strong_password"
        }

        ### Successful Response (201 Created)
        {
            "email": "user@example.com"
        }

        ### Error Response (400 Bad Request)
        {
            "password2": ["Passwords do not match."],
            "email": ["This field must be unique."]
        }

        ### Email Sent
        An activation email will be sent to the provided email address containing a JWT access token.
        """
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        """
                Handles the user registration and sends an activation token via email.

                - Validates the registration data using UserRegistrationSerializer.
                - If the data is valid:
                    - Creates the user.
                    - Generates a JWT token.
                    - Sends an activation email using a template and includes the token in the email context.
                - Returns appropriate success or error responses.

                Returns:
                    - 201 Created with user data if registration is successful.
                    - 400 Bad Request with validation errors if data is invalid.
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
    """
        CustomDiscardAuthToken handles the logout process by deleting the user's authentication token.

        This endpoint is used to log out an authenticated user by invalidating (deleting) their token.

        POST /accounts/api/v1/custom/token/logout/
        -------------------------------------------

        ### Authentication Required:
        - Yes (Token-based)

        ### Request Headers:
        Authorization: Token <user_token>

        ### Request Body:
        - None

        ### Successful Response (204 No Content):
        - Indicates the token was successfully deleted and the user is logged out.

        ### Error Response:
        - 401 Unauthorized: If the request does not include a valid authentication token.
        """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
                Handle POST request to log out the user by deleting their authentication token.

                - Requires the user to be authenticated.
                - Deletes the current user's token from the database.
                - Returns a 204 No Content response on success.

                Returns:
                    - 204 No Content on success.
                    - 401 Unauthorized if the user is not authenticated.
                """
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenPairView(TokenObtainPairView):
    """
        CustomTokenPairView provides JWT access and refresh tokens for authenticated users.

        This endpoint is used for logging in with email and password to obtain JWT tokens.

        POST /accounts/api/v1/custom/token/
        -----------------------------------

        ### Request Body (JSON):
        {
            "email": "user@example.com",
            "password": "user_password"
        }

        ### Successful Response (200 OK):
        {
            "refresh": "your_refresh_token",
            "access": "your_access_token"
        }

        ### Error Response (401 Unauthorized):
        {
            "detail": "No active account found with the given credentials"
        }

        ### Notes:
        - This view uses a custom serializer `CustomObtainPairSerializer` to customize login logic or token payload if needed.
        - It is based on `TokenObtainPairView` from `rest_framework_simplejwt.views`.
        """
    serializer_class = CustomObtainPairSerializer


class ChangePasswordView(UpdateAPIView):
    """
               ChangePasswordView allows an authenticated user to change their password.

               This endpoint requires the user to provide their current password and a new password.

               PUT /accounts/api/v1/change-password/
               --------------------------------------

               ### Authentication Required:
               - Yes (JWT or Token)

               ### Request Body (JSON):
               {
                   "old_password": "current_password",
                   "new_password": "new_secure_password"
               }

               ### Successful Response (200 OK):
               {
                   "message": "Password changed successfully"
               }

               ### Error Responses:
               - 400 Bad Request: If the old password is incorrect or validation fails.
               {
                   "old_password": "Your password is wrong"
               }

               ### Notes:
               - Only the authenticated user can change their own password.
               - Validation and password hashing are handled via the serializer and Django's built-in methods.
               """
    model = User
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self):

        """Returns the current authenticated user object."""
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        """
                Handle PUT request to change the authenticated user's password.

                Validates the old password and updates the password to the new one if valid.

                Returns:
                    - 200 OK on success
                    - 400 Bad Request on validation failure
                """
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
    """
        ProfileApiView allows an authenticated user to retrieve and update their profile.

        GET /accounts/api/v1/profile/
        PUT /accounts/api/v1/profile/

        --------------------------------------

        ### Authentication Required:
        - Yes (JWT or Token)

        ### GET Response (200 OK):
        {
            "id": 1,
            "user": 3,
            "bio": "About me...",
            "location": "City, Country",
            ...
        }

        ### PUT Request Body (JSON):
        {
            "bio": "Updated bio",
            "location": "New Location"
        }

        ### Successful PUT Response (200 OK):
        {
            "id": 1,
            "user": 3,
            "bio": "Updated bio",
            "location": "New Location"
        }

        ### Error Response (404 Not Found):
        {
            "detail": "Not found."
        }

        ### Notes:
        - This view uses `RetrieveUpdateAPIView` to support both reading and editing the profile.
        - The `get_queryset` method ensures users can only access or update their own profile.
        """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_queryset(self):
        """
                Override the default queryset to return only the current user's profile.
                """
        obj = get_object_or_404(Profile, pk=self.request.user.pk)
        return obj


class SendEmailView(GenericAPIView):
    """
        SendEmailView sends a test email to verify SMTP configuration (e.g., smtp4dev).

        GET /accounts/api/v1/send/email/

        --------------------------------------

        ### Purpose:
        This endpoint is used for testing the email sending functionality.
        It sends a plain test email to a predefined recipient using Django’s email backend.

        ### Authentication Required:
        - No

        ### Successful Response (200 OK):
        {
            "message": "email sent successfully"
        }

        ### Example Use Case:
        - Verifying that your SMTP service (like smtp4dev or Mailhog) is working correctly.
        - Useful during development to test email delivery.

        ### Notes:
        - The email content and recipients are hardcoded.
        - Make sure your SMTP settings (EMAIL_HOST, EMAIL_PORT, etc.) are correctly configured in `settings.py`.
        """

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
    """
        ActivationApiView handles user account activation via a JWT token.

        GET /accounts/api/v1/activation/confirm/<token>/

        --------------------------------------------------

        ### Purpose:
        This endpoint is used to verify and activate a newly registered user's account using a JWT token sent via email.

        ### Parameters:
        - token (str): A JWT token included in the URL. This token must contain a valid `user_id` payload.

        ### Process:
        1. The token is decoded using the project’s SECRET_KEY.
        2. If the token is valid and not expired, the user is retrieved using the ID from the token.
        3. The user's `is_verified` field is set to `True`.
        4. Returns a message indicating successful activation.

        ### Possible Responses:
        - 200 OK: Account successfully activated.
          ```json
          { "detail": "user has been activated" }
          ```
        - 400 Bad Request: If the token is invalid or expired.
          ```json
          { "detail": "invalid token" }
          ```
          or
          ```json
          { "detail": "token has been expired" }
          ```

        ### Notes:
        - Make sure the token you generate during registration includes the `user_id`.
        - Ensure `is_verified` is a valid field in your User model.
        """

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
    """
       ActivationResendApiView handles resending the JWT activation token to the user's email.

       POST /accounts/api/v1/activation/resend/
       ----------------------------------------

       ### Purpose:
       Allows a user to request a new activation token via email if the original one was lost, expired, or never received.

       ### Request Body (JSON):
       {
           "email": "user@example.com"
       }

       ### Process:
       1. Validates the provided email using the `ActivationResendSerializer`.
       2. If valid, generates a new refresh and access token for the associated user.
       3. Sends an email to the user with the activation token included in the message body and/or template context.

       ### Successful Response (200 OK):
       ```json
       {
           "message": "Token resent to your email"
       }
       ```

       ### Error Response (400 Bad Request):
       If the email is missing or invalid:
       ```json
       {
           "detail": "email is empty"
       }
       ```

       ### Notes:
       - Ensure the `ActivationResendSerializer` properly validates the email and returns the associated user instance.
       - The email is rendered using the template `email/activation_email.tpl`. Make sure this file exists and is properly configured.
       - Tokens are generated using `RefreshToken.for_user(user)`.
       """
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
