from django.db import models
from accounts.models import User

# Create your models here.
class Post(models.Model):
    """
    this is class to define posts for blog app
    """
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    auther = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    this is class to define categories for blog app
    """
    name = models.CharField(max_length=200)
