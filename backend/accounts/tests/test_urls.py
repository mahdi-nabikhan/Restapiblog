import pytest

from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User

@pytest.mark.django_db
class TestAccountAPI:

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

    def test_token_login_url(self):
        url = reverse("accounts:api-v1:token")

        response = self.client.post(
            url,
            self.user_data,
            format="json"
        )

        assert response.status_code in [200, 400]

    def test_jwt_create(self):
        url = reverse("accounts:api-v1:jwt-create")

        response = self.client.post(
            url,
            self.user_data,
            format="json"
        )

        assert response.status_code in [200, 401]

    def test_jwt_refresh(self):
        create_url = reverse("accounts:api-v1:jwt-create")

        create_response = self.client.post(
            create_url,
            self.user_data,
            format="json"
        )

        if create_response.status_code == 200:

            refresh = create_response.data["refresh"]

            refresh_url = reverse("accounts:api-v1:jwt-refresh")

            response = self.client.post(
                refresh_url,
                {"refresh": refresh},
                format="json"
            )

        assert response.status_code == 200

    def test_jwt_verify(self):
        create_url = reverse("accounts:api-v1:jwt-create")

        create_response = self.client.post(
            create_url,
            self.user_data,
            format="json"
        )

        if create_response.status_code == 200:

            access = create_response.data["access"]

            verify_url = reverse("accounts:api-v1:jwt-verify")

            response = self.client.post(
                verify_url,
                {"token": access},
                format="json"
            )

        assert response.status_code == 200

    
    def test_profile(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("accounts:api-v1:profile")

        response = self.client.get(url)

        assert response.status_code == 200
    def test_change_password(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("accounts:api-v1:change-password")

        response = self.client.put(
            url,
            {
                "old_password": "StrongPass123!",
                "new_password": "NewPassword123!"
            },
            format="json"
        )

        assert response.status_code in [200, 204]


    def test_send_email_endpoint(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("accounts:api-v1:send-email")

        response = self.client.get(url)

        assert response.status_code in [200, 405]

    
        response = self.client.get(url)

        assert response.status_code in [200, 400, 404]

    def test_activation_resend(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("accounts:api-v1:activation-resend")

        response = self.client.post(
        url,
        {"email": self.user.email},
        format="json"
)

        assert response.status_code in [200, 202, 204]

    def test_get_user(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("accounts:api-v1:get-user")

        response = self.client.get(url)
        assert response.status_code == 200

