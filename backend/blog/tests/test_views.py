import pytest
from django.urls import reverse
from rest_framework import status
from blog.models import Post, Category
from accounts.models import *
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestPostViews:
    def test_get_post_list(self, api_client):
        url = reverse('blog:api:post-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_post(self, api_client, django_user_model):
        user = django_user_model.objects.create_user(email='test@example.com', password='1234')
        api_client.force_authenticate(user=user)
        category = Category.objects.create(name='Test Category')

        url = reverse('blog:api:post-list')
        data = {
            'title': 'Test Post',
            'content': 'Content here',
            'category': category.id,
            'status': True,
        }

        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Test Post'

    def test_get_post_detail(self, api_client, django_user_model):
        user = django_user_model.objects.create_user(email='john@example.com', password='1234')
        category = Category.objects.create(name='Cat1')
        post = Post.objects.create(title='Title', content='Content', category=category, auther=user, status=True)

        url = reverse('blog:api:post-detail', kwargs={'pk': post.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == post.title

    def test_patch_post_detail(self, api_client, django_user_model):
        user = django_user_model.objects.create_user(email='john@example.com', password='1234')
        category = Category.objects.create(name='Patch Cat')
        post = Post.objects.create(title='Old', content='...', category=category, auther=user, status=True)

        api_client.force_authenticate(user=user)
        url = reverse('blog:api:post-detail', kwargs={'pk': post.pk})
        response = api_client.patch(url, {'title': 'New Title'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'New Title'

    def test_delete_post_detail(self, api_client, django_user_model):
        user = django_user_model.objects.create_user(email='delete@example.com', password='1234')
        category = Category.objects.create(name='Cat')
        post = Post.objects.create(title='ToDelete', content='...', category=category, auther=user, status=True)

        api_client.force_authenticate(user=user)
        url = reverse('blog:api:post-detail', kwargs={'pk': post.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestPostViewSet:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(email='testuser', password='testpass')

    @pytest.fixture
    def api_client_auth(self, api_client, user):
        api_client.force_authenticate(user=user)
        return api_client

    def test_list_posts(self, api_client_auth):
        url = reverse('blog:api:post-list')  # از نام درست استفاده کن
        response = api_client_auth.get(url)
        assert response.status_code == 200

    def test_create_post(self, api_client_auth, user):
        url = reverse('blog:api:post-list')
        data = {
            "title": "Test Post",
            "content": "Test content",
            "auther": user.pk,
        }
        response = api_client_auth.post(url, data, format='json')
        assert response.status_code == 201
        assert response.data['title'] == "Test Post"

    def test_retrieve_post(self, api_client_auth, user):
        post = Post.objects.create(title="Test Post", content="Content", auther=user)
        url = reverse('blog:api:post-detail', kwargs={'pk': post.pk})
        response = api_client_auth.get(url)
        assert response.status_code == 200
        assert response.data['title'] == post.title

    def test_update_post(self, api_client_auth, user):
        post = Post.objects.create(title="Old Title", content="Old Content", auther=user)
        url = reverse('blog:api:post-detail', kwargs={'pk': post.pk})
        data = {
            "title": "New Title",
            "content": "New Content",
            "auther": user.pk,
        }
        response = api_client_auth.put(url, data, format='json')
        assert response.status_code == 200
        assert response.data['title'] == "New Title"

    def test_partial_update_post(self, api_client_auth, user):
        post = Post.objects.create(title="Old Title", content="Old Content", auther=user)
        url = reverse('blog:api:post-detail', kwargs={'pk': post.pk})
        data = {
            "title": "Partial New Title",
        }
        response = api_client_auth.patch(url, data, format='json')
        assert response.status_code == 200
        assert response.data['title'] == "Partial New Title"

    def test_delete_post(self, api_client_auth, user):
        post = Post.objects.create(title="To be deleted", content="Content", auther=user)
        url = reverse('blog:api:post-detail', kwargs={'pk': post.pk})
        response = api_client_auth.delete(url)
        assert response.status_code == 204
        assert Post.objects.filter(pk=post.pk).count() == 0


@pytest.fixture
def api_client():
    return APIClient()
