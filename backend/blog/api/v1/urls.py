from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

app_name = "api"
router = DefaultRouter()
router.register(r"posts", PostAPIActionViewSets, basename="post")
urlpatterns = [
    path("post/", PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path(
        "comments/<int:pk>/",
        CommentListAndCreateAPIView.as_view(),
        name="comments-list-create",
    ),
    path(
        "comment/detail/<int:pk>/",
        CommentDetailAndDeleteAPIView.as_view(),
        name="comment-detail",
    ),
    path("user/post/", UserPostListApiView.as_view(), name="user-posts"),
    path("post/list/cache/", PostListCacheAPIView.as_view(), name="post-cache"),
    path("img/post/<int:pk>/", PostImageCreateAndListAPIView.as_view(), name="img_post"),
    path("", include(router.urls)),
]
