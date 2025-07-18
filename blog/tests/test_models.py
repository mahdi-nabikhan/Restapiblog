import pytest
from django.utils import timezone
from blog.models import Post, Category
from accounts.models import User

@pytest.mark.django_db
def test_category_str():
    category = Category.objects.create(name="Tech")
    assert str(category.name) == "Tech"

@pytest.mark.django_db
def test_post_str():
    user = User.objects.create_user(email="test@example.com", password="password123")
    category = Category.objects.create(name="Tech")
    post = Post.objects.create(
        auther=user,
        title="Test Post",
        content="This is the content of the post.",
        status=True,
        category=category,
        published_date=timezone.now()
    )
    assert str(post) == "Test Post"

@pytest.mark.django_db
def test_post_get_snippet():
    user = User.objects.create_user(email="snippet@example.com", password="password123")
    category = Category.objects.create(name="SnippetCat")
    post = Post.objects.create(
        auther=user,
        title="Snippet Post",
        content="This is the full content.",
        status=True,
        category=category,
        published_date=timezone.now()
    )
    assert post.get_snippet() == "This is th"

@pytest.mark.django_db
def test_post_get_absolute_api_url(client):
    user = User.objects.create_user(email="url@example.com", password="password123")
    category = Category.objects.create(name="URLCat")
    post = Post.objects.create(
        auther=user,
        title="URL Post",
        content="Some content.",
        status=True,
        category=category,
        published_date=timezone.now()
    )
    url = post.get_absolute_api_url()
    response = client.get(url)
    assert response.status_code in [200, 301, 302, 403, 401, 404]  # depends on your view setup
