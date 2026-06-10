from unittest.mock import patch

import jwt
import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


@pytest.mark.django_db
class TestSendTokenActivationRegisterView:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.url = reverse('accounts:api-v1:token-register')

    def test_register_user_success_and_email_sent(self):
        data = {
            "email": "testuser@example.com",
            "password": "StrongPassword123!",
            "password2": "StrongPassword123!"
        }

        with patch('mail_templated.EmailMessage.send') as mock_send:
            response = self.client.post(self.url, data, format='json')

            assert response.status_code == 201
            assert response.data['email'] == data['email']
            assert User.objects.filter(email=data['email']).exists()
            mock_send.assert_called_once()

    def test_register_user_passwords_do_not_match(self):
        data = {
            "email": "testuser2@example.com",
            "password": "Password1",
            "password2": "Password2"
        }

        response = self.client.post(self.url, data, format='json')

        assert response.status_code == 400
        assert 'password2' in response.data
        assert 'Passwords do not match' in response.data['password2'][0]

    def test_register_user_email_already_exists(self):
        User.objects.create_user(email="duplicate@example.com", password="somepass")

        data = {
            "email": "duplicate@example.com",
            "password": "Password1",
            "password2": "Password1"
        }
        response = self.client.post(self.url, data, format='json')

        assert response.status_code == 400
        assert 'email' in response.data


@pytest.mark.django_db
class TestRegisterView:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('accounts:api-v1:register')

    def test_register_user_success(self):
        data = {
            "email": "newuser@example.com",
            "password": "strong_password123",
            "password2": "strong_password123"
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == 201
        assert response.data['email'] == data['email']

    def test_register_password_mismatch(self):
        data = {
            "email": "newuser@example.com",
            "password": "password1",
            "password2": "password2"
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == 400
        assert 'password2' in response.data

    def test_register_missing_password(self):
        data = {
            "email": "newuser@example.com",
            # "password" حذف شده
            "password2": "anything"
        }
        response = self.client.post(self.url, data, format='json')
        assert response.status_code == 400
        assert 'password' in response.data


@pytest.mark.django_db
class TestCustomObtainToken(APITestCase):
    def setUp(self):
        self.url = reverse('accounts:api-v1:custom-token')
        self.password = 'StrongPass123!'
        self.user = User.objects.create_user(email='testuser@example.com', password=self.password)

    def test_login_success(self):
        data = {
            "email": self.user.email,
            "password": self.password
        }
        response = self.client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data
        assert response.data['email'] == self.user.email
        assert response.data['user_id'] == self.user.id

    def test_login_invalid_password(self):
        data = {
            "email": self.user.email,
            "password": "WrongPassword123"
        }
        response = self.client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data

    def test_login_nonexistent_user(self):
        data = {
            "email": "nonexistent@example.com",
            "password": "AnyPassword123"
        }
        response = self.client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data


@pytest.mark.django_db
class TestCustomObtainToken(APITestCase):
    def setUp(self):
        self.url = reverse('accounts:api-v1:custom-token')
        self.email = 'test@example.com'
        self.password = 'StrongPass123'
        self.user = User.objects.create_user(email=self.email, password=self.password)

    def test_login_successful(self):
        data = {
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data
        assert response.data['email'] == self.email
        assert response.data['user_id'] == self.user.id

    def test_login_wrong_password(self):
        data = {
            "email": self.email,
            "password": "WrongPassword"
        }
        response = self.client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data

    def test_login_nonexistent_email(self):
        data = {
            "email": "notfound@example.com",
            "password": "Whatever123"
        }
        response = self.client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data


@pytest.mark.django_db
class TestSendEmailView(APITestCase):
    def setUp(self):
        self.url = reverse('accounts:api-v1:send_templated_email')  #

    @patch('django.core.mail.send_mail')
    def test_send_email_successfully(self, mock_send_mail):
        mock_send_mail.return_value = 1

        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["massage"] == "email send successfully "


@pytest.mark.django_db
class TestSendEmailApiView:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="mmd@gmail.com", password="pass123")
        self.url = reverse("accounts:api-v1:send-email")

    @patch("accounts.views.EmailMessage.send")
    def test_send_email_successfully(self, mock_send):
        mock_send.return_value = 1
        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Token sent via email"
        mock_send.assert_called_once()


@pytest.mark.django_db
class TestActivationApiView:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="active@example.com", password="pass123", is_verified=False)

    def test_activate_user_valid_token(self):
        token = RefreshToken.for_user(self.user).access_token
        url = reverse("accounts:api-v1:activation-confirm", kwargs={"token": str(token)})
        response = self.client.get(url)

        self.user.refresh_from_db()
        assert response.status_code == 200
        assert self.user.is_verified is True
        assert "activated" in response.data["detail"].lower()

    def test_activate_user_invalid_token(self):
        url = reverse("accounts:api-v1:activation-confirm", kwargs={"token": "invalidtoken"})
        response = self.client.get(url)
        assert response.status_code == 400
        assert "invalid token" in response.data["detail"].lower()

    def test_activate_user_expired_token(self):
        payload = {"user_id": self.user.id, "exp": 0}
        expired_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        url = reverse("accounts:api-v1:activation-confirm", kwargs={"token": expired_token})
        response = self.client.get(url)
        assert response.status_code == 400
        assert "expired" in response.data["detail"].lower()



