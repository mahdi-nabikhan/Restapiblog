import pytest
from django.urls import reverse
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import User


@pytest.mark.django_db
class TestAccountAPI:

    @pytest.fixture(autouse=True)
    def disable_throttle(self):
        with override_settings(
            REST_FRAMEWORK={
                "DEFAULT_THROTTLE_CLASSES": [],
                "DEFAULT_THROTTLE_RATES": {},
            }
        ):
            yield

    def setup_method(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="user@example.com",
            password="StrongPass123!"
        )

        self.user_data = {
            "email": "user@example.com",
            "password": "StrongPass123!"
        }

    # -------------------------
    # REGISTER
    # -------------------------
    def test_register_success(self):
        url = reverse("accounts:api-v1:register")

        data = {
            "email": "newuser@example.com",
            "password": "Testpass123!",
            "password2": "Testpass123!"
        }

        response = self.client.post(url, data)

        assert response.status_code in [200, 201]

    # -------------------------
    # TOKEN LOGIN
    # -------------------------
    def test_token_login_success(self):
        url = reverse("accounts:api-v1:token")

        response = self.client.post(url, self.user_data)

        assert response.status_code == 200
        assert "token" in response.data

    def test_token_discard(self):
        url = reverse("accounts:api-v1:token")
        res = self.client.post(url, self.user_data)

        token = res.data.get("token")
        assert token is not None

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        url = reverse("accounts:api-v1:discard-token")
        response = self.client.post(url)

        assert response.status_code in [200, 204]

    # -------------------------
    # JWT
    # -------------------------
    def test_jwt_create(self):
        url = reverse("accounts:api-v1:jwt-create")

        response = self.client.post(url, self.user_data)

        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_jwt_refresh(self):
        url = reverse("accounts:api-v1:jwt-create")
        res = self.client.post(url, self.user_data)

        refresh = res.data["refresh"]

        url = reverse("accounts:api-v1:jwt-refresh")
        response = self.client.post(url, {"refresh": refresh})

        assert response.status_code == 200
        assert "access" in response.data

    def test_jwt_verify(self):
        url = reverse("accounts:api-v1:jwt-create")
        res = self.client.post(url, self.user_data)

        access = res.data["access"]

        url = reverse("accounts:api-v1:jwt-verify")
        response = self.client.post(url, {"token": access})

        assert response.status_code == 200

    # -------------------------
    # PROFILE
    # -------------------------
    def test_profile(self):
        url = reverse("accounts:api-v1:profile")

        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)

        assert response.status_code == 200

    # -------------------------
    # CHANGE PASSWORD
    # -------------------------
    def test_change_password(self):
        url = reverse("accounts:api-v1:change-password")

        self.client.force_authenticate(user=self.user)

        data = {
            "old_password": "StrongPass123!",
            "new_password": "NewStrong123!"
        }

        response = self.client.put(url, data)

        assert response.status_code in [200, 204]

    # -------------------------
    # EMAIL
    # -------------------------
    def test_send_email(self):
        url = reverse("accounts:api-v1:send-email")

        self.client.force_authenticate(user=self.user)

        data = {
            "subject": "Hello",
            "message": "Test message",
            "to": "test@example.com"
        }

        response = self.client.post(url, data)

        assert response.status_code in [200, 202, 204]

    def test_send_templated_email(self):
        url = reverse("accounts:api-v1:send_templated_email")

        self.client.force_authenticate(user=self.user)

        data = {
            "template_name": "welcome",
            "to": "test@example.com"
        }

        response = self.client.post(url, data)

        assert response.status_code in [200, 202, 204]

    # -------------------------
    # ACTIVATION
    # -------------------------
    def test_activation_confirm(self):
        url = reverse(
            "accounts:api-v1:activation-confirm",
            args=["dummy-token"]
        )

        response = self.client.get(url)

        assert response.status_code in [200, 204]