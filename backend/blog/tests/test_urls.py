import pytest
from django.urls import reverse
from blog.models import Post
from accounts.models import *
from rest_framework.test import APIClient



@pytest.mark.django_db
class TestClassicPostViews:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(email='testuser', password='testpass')

    @pytest.fixture
    def api_client_auth(self, api_client, user):
        api_client.force_authenticate(user=user)
        return api_client

    def test_post_list_view(self, api_client_auth):
        url = reverse('blog:api:post-list')  # maps to 'post/'
        response = api_client_auth.get(url)
        assert response.status_code == 200
        assert isinstance(response.data, list)

    def test_post_detail_view(self, api_client_auth, user):
        post = Post.objects.create(title="Classic View Post", content="content", auther=user)
        url = reverse('blog:api:post-detail', kwargs={'pk': post.pk})  # maps to 'post/<pk>/'
        response = api_client_auth.get(url)
        assert response.status_code == 200
        assert response.data['title'] == post.title


@pytest.mark.django_db
class TestPostViewSet:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(email='testuser', password='testpass')

    @pytest.fixture
    def api_client_auth(self, api_client, user):
        api_client.force_authenticate(user=user)
        return api_client

    def test_post_list_viewset(self, api_client_auth):
        url = reverse('blog:api:post-list')  # از router => posts/
        response = api_client_auth.get(url)
        assert response.status_code == 200
        assert isinstance(response.data, list)

    def test_post_create_viewset(self, api_client_auth, user):
        url = reverse('blog:api:post-list')
        data = {
            "title": "ViewSet Post",
            "content": "Content",
            "auther": user.pk,
        }
        response = api_client_auth.post(url, data, format='json')
        assert response.status_code == 201
        assert response.data['title'] == "ViewSet Post"

    def test_post_retrieve_viewset(self, api_client_auth, user):
        post = Post.objects.create(title="ViewSet Retrieve", content="Content", auther=user)
        url = reverse('blog:api:post-detail', kwargs={'pk': post.pk})
        response = api_client_auth.get(url)
        assert response.status_code == 200
        assert response.data['title'] == post.title

    def test_post_partial_update_viewset(self, api_client_auth, user):
        post = Post.objects.create(title="Partial Update", content="Old content", auther=user)
        url = reverse('blog:api:post-detail', kwargs={'pk': post.pk})
        data = {"title": "Updated Partial"}
        response = api_client_auth.patch(url, data, format='json')
        assert response.status_code == 200
        assert response.data['title'] == "Updated Partial"

    def test_post_delete_viewset(self, api_client_auth, user):
        post = Post.objects.create(title="Delete Me", content="content", auther=user)
        url = reverse('blog:api:post-detail', kwargs={'pk': post.pk})
        response = api_client_auth.delete(url)
        assert response.status_code == 204
        assert not Post.objects.filter(pk=post.pk).exists()


@pytest.fixture
def api_client():
    return APIClient()
