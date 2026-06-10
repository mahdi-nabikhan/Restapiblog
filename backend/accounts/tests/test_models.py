import pytest
from accounts.models import User, Profile

@pytest.mark.django_db
class TestUserModel:

    def test_create_user_success(self):
        user = User.objects.create_user(email="test@example.com", password="securepassword")
        assert user.email == "test@example.com"
        assert user.check_password("securepassword") is True
        assert user.is_active is True
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_superuser_success(self):
        admin = User.objects.create_superuser(email="admin@example.com", password="adminpass")
        assert admin.is_superuser is True
        assert admin.is_staff is True
        assert admin.is_active is True

    def test_create_user_without_email_raises_error(self):
        with pytest.raises(ValueError):
            User.objects.create_user(email=None, password="123456")

    def test_user_str_method(self):
        user = User.objects.create_user(email="struser@example.com", password="123456")
        assert str(user) == "struser@example.com"


@pytest.mark.django_db
class TestProfileModel:

    def test_profile_created_on_user_creation(self):
        user = User.objects.create_user(email="profiletest@example.com", password="pass")
        profile = Profile.objects.get(user=user)
        assert profile.user == user

    def test_profile_str_method(self):
        user = User.objects.create_user(email="profileuser@example.com", password="pass")
        profile = Profile.objects.get(user=user)
        assert str(profile) == "profileuser@example.com"
