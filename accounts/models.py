from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Permission, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    """
    custom user model manager where email  are the unique
    for authentication instead of usernames.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        self.create_user(email, password, **extra_fields)


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email instead of username.
    """
    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    created_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    """
    Represents additional information about a user.

    Each Profile is associated with one User and contains personal details
    such as first name, last name, profile image, and a description.

    Attributes:
        user (ForeignKey): Reference to the related User object.
        first_name (CharField): The user's first name.
        last_name (CharField): The user's last name.
        image (ImageField): An optional image field for user avatars.
        description (TextField): A short bio or description.
        created_date (DateTimeField): The datetime the profile was created.
        updated_date (DateTimeField): The datetime the profile was last updated.

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    """
    Signal receiver that automatically creates a Profile instance
    whenever a new User is created.

    Args:
        sender (Model): The model class that sent the signal (User).
        instance (User): The actual instance being saved.
        created (bool): Whether this is a new instance.
        **kwargs: Additional keyword arguments.
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        Profile.objects.create(user=instance)
