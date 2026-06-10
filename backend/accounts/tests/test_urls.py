import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import User  

@pytest.mark.django_db
class TestAccountEndpoints:

    def setup_method(self):
        self.client = APIClient()
        self.user_data = {
            "email": "user@example.com",
            "password": "StrongPass123!"
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_register_view(self):
        url = reverse('accounts:api-v1:register')
        data = {
            "email": "newuser@example.com",
            "password": "Testpass123!",
            "password2": "Testpass123!"
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_send_token_activation(self):
        url = reverse('accounts:api-v1:token-register')
        data = {"email": self.user.email}
        response = self.client.post(url, data)
        assert response.status_code in [200, 204]

    def test_obtain_token(self):
        url = reverse('accounts:api-v1:token')
        response = self.client.post(url, self.user_data)
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data

    def test_custom_token_obtain(self):
        url = reverse('accounts:api-v1:custom-token')
        response = self.client.post(url, self.user_data)
        assert response.status_code == status.HTTP_200_OK

    def test_discard_token(self):
        login_url = reverse('accounts:api-v1:token')
        token_response = self.client.post(login_url, self.user_data)
        token = token_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        discard_url = reverse('accounts:api-v1:discard-token')
        response = self.client.post(discard_url)
        assert response.status_code in [200, 204]

    def test_jwt_create(self):
        url = reverse('accounts:api-v1:jwt-create')
        response = self.client.post(url, self.user_data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    def test_jwt_refresh(self):
        jwt_url = reverse('accounts:api-v1:jwt-create')
        jwt_response = self.client.post(jwt_url, self.user_data)
        refresh_token = jwt_response.data['refresh']
        refresh_url = reverse('accounts:api-v1:jwt-refresh')
        response = self.client.post(refresh_url, {'refresh': refresh_token})
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    def test_jwt_verify(self):
        jwt_url = reverse('accounts:api-v1:jwt-create')
        jwt_response = self.client.post(jwt_url, self.user_data)
        access_token = jwt_response.data['access']
        verify_url = reverse('accounts:api-v1:jwt-verify')
        response = self.client.post(verify_url, {'token': access_token})
        assert response.status_code == status.HTTP_200_OK

    def test_jwt_custom(self):
        url = reverse('accounts:api-v1:jwt-custom')
        response = self.client.post(url, self.user_data)
        assert response.status_code == status.HTTP_200_OK

    def test_change_password(self):
        url = reverse('accounts:api-v1:change-password')
        self.client.force_authenticate(user=self.user)
        data = {
            "old_password": "StrongPass123!",
            "new_password": "NewStrong123!"
        }
        response = self.client.put(url, data)
        assert response.status_code in [200, 204]

    def test_profile_view(self):
        url = reverse('accounts:api-v1:profile')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_send_email(self):
        url = reverse('accounts:api-v1:send-email')
        self.client.force_authenticate(user=self.user)
        data = {
            "subject": "Hello",
            "message": "Test message",
            "to": "recipient@example.com"
        }
        response = self.client.post(url, data)
        assert response.status_code in [200, 202, 204]

    def test_send_email_template(self):
        url = reverse('accounts:api-v1:send_templated_email')
        self.client.force_authenticate(user=self.user)
        data = {
            "template_name": "welcome",
            "to": "recipient@example.com"
        }
        response = self.client.post(url, data)
        assert response.status_code in [200, 202, 204]

    def test_activation_confirm(self):

        token = "dummy-token"
        url = reverse('accounts:api-v1:activation-confirm', args=[token])
        response = self.client.get(url)
        assert response.status_code in [200, 204]
