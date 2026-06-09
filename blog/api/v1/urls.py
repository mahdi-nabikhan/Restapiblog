from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
app_name = 'api'
router = DefaultRouter()
router.register(r'posts', PostAPIActionViewSets, basename='post')
urlpatterns = [
    path('post/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/<int:pk>/',CommentListAndCreateAPIView.as_view(),name='comments-list-create'),
    path('', include(router.urls)),

]
