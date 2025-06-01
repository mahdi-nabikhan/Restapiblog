from typing import Any

from django.core.exceptions import ValidationError
from rest_framework import serializers
from accounts.models import *
from django.contrib.auth.password_validation import validate_password
from accounts.models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
        Serializer for user registration.

        Validates that:
        - Password and password confirmation match
        - Email is not already registered
        - Password meets Django's strength requirements

        On success, creates a new user instance using `create_user()`.
        """
    password2 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        email = data['email']
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Passwords do not match'})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already registered'})

        try:
            validate_password(data.get('password'))
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})  # `e.messages` is a list
        return data


class CustomAuthTokenSerializer(serializers.Serializer):
    """
        Serializer for authenticating users with email and password.

        Validates user credentials using Django's `authenticate` method.
        On successful authentication, the authenticated user is attached to the
        validated data under the 'user' key.
        """
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomObtainPairSerializer(TokenObtainPairSerializer):
    """
     CustomObtainPairSerializer extends the default TokenObtainPairSerializer
     to include additional user information in the token response.

     Purpose:
     --------
     When a user successfully authenticates, this serializer will return
     the default 'access' and 'refresh' tokens, along with the user's email
     and user ID.

     Example Response:
     -----------------
     {
         "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOi...",
         "access": "eyJ0eXAiOiJKV1QiLCJhbGciOi...",
         "email": "user@example.com",
         "user_id": 5
     }

     Notes:
     ------
     - This serializer is typically used with a custom TokenObtainPairView.
     - Make sure your user model has an `email` field accessible via `self.user.email`.
     """

    def validate(self, attrs):

        validated_data = super().validate(attrs)
        validated_data['email'] = self.user.email
        validated_data['user_id'] = self.user.id
        return validated_data


class ChangePasswordSerializer(serializers.Serializer):
    """
        Serializer for handling password change requests.

        Fields:
        -------
        old_password: str
            The user's current password. Required.
        new_password: str
            The new password the user wants to set. Required.
        new_password1: str
            Confirmation of the new password. Must match new_password. Required.

        Validation:
        -----------
        - Checks that new_password and new_password1 match.
        - Validates the new_password against Django's password validation rules.
          If validation fails, returns the corresponding error messages.

        Usage:
        ------
        Use this serializer to validate and update the user's password in password
        change endpoints.
        """
    old_password = serializers.CharField(max_length=255, required=True)
    new_password = serializers.CharField(max_length=255, required=True)
    new_password1 = serializers.CharField(max_length=255, required=True)

    def validate(self, data):
        if data['new_password'] != data['new_password1']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})

        try:
            validate_password(data.get('new_password'))
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})  # `e.messages` is a list
        return data


class ProfileSerializer(serializers.ModelSerializer):
    """
        Serializer for the Profile model.

        This serializer includes all fields of the Profile model.
        The 'user' field is set as read-only to prevent modification.

        Usage:
        ------
        Used for retrieving and updating user profile information.
        """
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('user',)


class ActivationResendSerializer(serializers.Serializer):
    """
        Serializer for resending the activation token via email.

        Fields:
        -------
        email: EmailField
            The user's email address. Required.

        Validation:
        -----------
        - Checks if the email is registered in the system.
        - Ensures the user's email is not already verified.
        - Attaches the user object to validated data for further processing.

        Usage:
        ------
        Used in endpoints that resend activation tokens to users who haven't
        verified their accounts yet.
        """
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user_obj = User.objects.get(email=email)

        except User.DoesNotExist:
            raise serializers.ValidationError({'email': 'Email not registered'})
        if user_obj.is_verified:
            raise serializers.ValidationError({'email': 'Email already verified'})

        attrs['user'] = user_obj
        return super().validate(attrs)
