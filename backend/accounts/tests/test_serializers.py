import pytest
from django.core.exceptions import ValidationError
from accounts.models import User, Profile
from accounts.api.v1.serializers import (
    UserRegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    ActivationResendSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestUserRegistrationSerializer:

    def test_valid_data_creates_user(self):
        data = {
            "email": "testuser@example.com",
            "password": "StrongPass123!",
            "password2": "StrongPass123!",
        }
        serializer = UserRegistrationSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        user = serializer.save()
        assert user.email == data["email"]
        assert user.check_password(data["password"])

    def test_password_mismatch(self):
        data = {
            "email": "testuser@example.com",
            "password": "pass1",
            "password2": "pass2",
        }
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()
        assert "password2" in serializer.errors

    def test_email_already_registered(self, django_user_model):
        django_user_model.objects.create_user(email="exists@example.com", password="pass123")
        data = {
            "email": "exists@example.com",
            "password": "StrongPass123!",
            "password2": "StrongPass123!",
        }
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_password_strength_validation(self):
        data = {
            "email": "test@example.com",
            "password": "123",  # weak password
            "password2": "123",
        }
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()
        assert "password" in serializer.errors


@pytest.mark.django_db
class TestCustomAuthTokenSerializer:

    def test_valid_credentials(self, django_user_model):
        user = django_user_model.objects.create_user(email="auth@example.com", password="pass123")
        data = {"email": "auth@example.com", "password": "pass123"}
        serializer = CustomAuthTokenSerializer(data=data, context={"request": None})
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data["user"] == user

    def test_invalid_credentials(self):
        data = {"email": "noone@example.com", "password": "wrong"}
        serializer = CustomAuthTokenSerializer(data=data, context={"request": None})
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors or "authorization" in serializer.errors


@pytest.mark.django_db
class TestCustomObtainPairSerializer:

    def test_token_contains_user_info(self, django_user_model):
        user = django_user_model.objects.create_user(email="jwtuser@example.com", password="pass123")
        serializer = CustomObtainPairSerializer(data={"email": user.email, "password": "pass123"})
        assert serializer.is_valid(), serializer.errors
        data = serializer.validated_data
        assert "access" in data
        assert "refresh" in data
        assert data["email"] == user.email
        assert data["user_id"] == user.id


@pytest.mark.django_db
class TestChangePasswordSerializer:

    def test_valid_password_change(self):
        data = {
            "old_password": "oldpass123",
            "new_password": "NewStrongPass123!",
            "new_password1": "NewStrongPass123!",
        }
        serializer = ChangePasswordSerializer(data=data)
        assert serializer.is_valid()

    def test_password_mismatch(self):
        data = {
            "old_password": "oldpass123",
            "new_password": "pass1",
            "new_password1": "pass2",
        }
        serializer = ChangePasswordSerializer(data=data)
        assert not serializer.is_valid()
        assert "password" in serializer.errors

    def test_password_strength_validation(self):
        data = {
            "old_password": "oldpass123",
            "new_password": "123",
            "new_password1": "123",
        }
        serializer = ChangePasswordSerializer(data=data)
        assert not serializer.is_valid()
        assert "password" in serializer.errors


@pytest.mark.django_db
class TestProfileSerializer:

    def test_serialize_profile(self, django_user_model):
        user = django_user_model.objects.create_user(email="profiletest@example.com", password="pass123")
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(instance=profile)
        data = serializer.data
        assert data["user"] == user.id


@pytest.mark.django_db
class TestActivationResendSerializer:

    def test_valid_email_not_verified(self, django_user_model):
        user = django_user_model.objects.create_user(email="notverified@example.com", password="pass123", is_verified=False)
        serializer = ActivationResendSerializer(data={"email": user.email})
        assert serializer.is_valid()
        assert serializer.validated_data["user"] == user

    def test_email_not_registered(self):
        serializer = ActivationResendSerializer(data={"email": "nonexistent@example.com"})
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_email_already_verified(self, django_user_model):
        user = django_user_model.objects.create_user(email="verified@example.com", password="pass123", is_verified=True)
        serializer = ActivationResendSerializer(data={"email": user.email})
        assert not serializer.is_valid()
        assert "email" in serializer.errors
