import pytest
from django.urls import reverse
from rest_framework import status
from blog.models import Post, Category


@pytest.mark.django_db
class TestPostListView:
    def test_get_post_list(self, api_client):
        url = reverse('blog:api:post-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_post(self, api_client, django_user_model):
        user = django_user_model.objects.create_user(email='testuser', password='1234')
        api_client.force_authenticate(user=user)

        category = Category.objects.create(name='Test Category')
        url = reverse('blog:api:post-list')
        data = {
            'title': 'Test Post',
            'content': 'Some content',
            'category': category.id,
            'status': True,
        }

        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Test Post'


@pytest.mark.django_db
class TestPostDetailView:
    def test_get_post_detail(self, api_client, django_user_model):
        user = django_user_model.objects.create_user(email='john', password='1234')
        category = Category.objects.create(name='Detail Category')
        post = Post.objects.create(
            title='Detail Post',
            content='Detail content',
            category=category,
            auther=user,
            status=True
        )
        url = reverse('blog:api:post-detail', kwargs={'pk': post.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == post.title

    def test_put_post_detail(self, api_client, django_user_model):
        user = django_user_model.objects.create_user(email='john', password='1234')
        category = Category.objects.create(name='Put Category')
        post = Post.objects.create(
            title='Original Title',
            content='Original content',
            category=category,
            auther=user,
            status=True
        )
        api_client.force_authenticate(user=user)
        url = reverse('blog:api:post-detail', kwargs={'pk': post.pk})
        data = {
            'title': 'Updated Title',
            'content': 'Updated content',
            'category': category.id,
            'status': True,
        }
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Title'

    def test_patch_post_detail(self, api_client, django_user_model):
        user = django_user_model.objects.create_user(email='john', password='1234')
        category = Category.objects.create(name='Patch Category')
        post = Post.objects.create(
            title='Patch Title',
            content='Patch content',
            category=category,
            auther=user,
            status=True
        )
        api_client.force_authenticate(user=user)
        url = reverse('blog:api:post-detail', kwargs={'pk': post.pk})
        response = api_client.patch(url, {'title': 'New Title'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'New Title'

    def test_delete_post_detail(self, api_client, django_user_model):
        user = django_user_model.objects.create_user(email='john', password='1234')
        category = Category.objects.create(name='Delete Cat')
        post = Post.objects.create(
            title='Delete Me',
            content='Bye',
            category=category,
            auther=user,
            status=True
        )
        api_client.force_authenticate(user=user)
        url = reverse('blog:api:post-detail', kwargs={'pk': post.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()
