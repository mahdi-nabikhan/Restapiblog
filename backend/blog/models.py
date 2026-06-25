from django.db import models
from accounts.models import User
from django.urls import reverse
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


    def get_snippet(self):
        return self.content[:10]

    def get_absolute_api_url(self):
        return reverse('blog:api:post-detail',args=[self.pk])


class Category(models.Model):
    """
    this is class to define categories for blog app
    """
    name = models.CharField(max_length=200)
    
    
    
class Comments(models.Model):
    """a model for commnets of a post """
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    
    content = models.TextField(max_length=255)
    published = models.BooleanField(default=False)
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class PostImages(models.Model):
    """ this is model for create and store more images related with single posts"""
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images/')
    
    