from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import *
from blog.models import *
from rest_framework.viewsets import ViewSet
from .permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import DefaultPagination
from django.core.cache import cache
import random
from django.shortcuts import get_object_or_404
from documents import PostDocument

class PostListView(GenericAPIView):
    """
    get:
    Return a list of all blog posts.

    Returns:
        - 200 OK: A list of serialized post objects.

    post:
    Create a new blog post with the provided data.

    Request Body:
        {
            "title": "Post Title",
            "content": "Post Content",
            ...
        }

    Returns:
        - 201 Created: The newly created post object.
        - 400 Bad Request: Validation errors in the provided data.
    """

    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ["title", "auther"]
    search_fields = ["title", "content"]
    ordering_fields = "title"
    pagination_class = DefaultPagination
    queryset = Post.objects.all()

    def get(self, request):
        post_obj = self.get_queryset()
        serializer = self.serializer_class(
            post_obj, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(GenericAPIView):
    """
    get:
    Retrieve a single post by its ID.

    Returns:
        - 200 OK: The post was found and returned.
        - 404 Not Found: No post matches the given ID.

    put:
    Fully update a post with the provided data.

    Request Body:
        {
            "title": "New Title",
            "content": "Updated content",
            ...
        }

    Returns:
        - 200 OK: Post updated successfully.
        - 400 Bad Request: Validation errors.

    patch:
    Partially update a post with the provided data.

    Returns:
        - 200 OK: Post updated successfully.
        - 400 Bad Request: Validation errors.

    delete:
    Delete a post by its ID.

    Returns:
        - 204 No Content: Post deleted.
        - 404 Not Found: No post matches the given ID.
    """

    serializer_class = PostSerializer
    model = Post
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ["title", "auther"]
    ordering_fields = "title"
    queryset = Post.objects.all()

    def get(self, request, pk):
        post_obj = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(post_obj, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post_obj = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(
            instance=post_obj, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        serializer = self.serializer_class(
            instance=self.model.objects.get(pk=pk),
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostAPIActionViewSets(ViewSet):
    """
    A ViewSet for performing CRUD operations on Post objects.

    list:
    Return a list of all blog posts.
    - Returns: 200 OK and a list of serialized posts.

    create:
    Create a new blog post.
    - Request body: JSON object with post data.
    - Returns: 201 Created and the created post, or 400 Bad Request on error.

    retrieve:
    Return a single blog post by its primary key (pk).
    - Returns: 200 OK and the post data.

    update:
    Replace an existing blog post with the provided data.
    - Request body: Full JSON post object.
    - Returns: 200 OK and the updated post, or 400 Bad Request on error.

    partial_update:
    Partially update a blog post.
    - Request body: Partial JSON data to update.
    - Returns: 200 OK and the updated post, or 400 Bad Request on error.

    destroy:
    Delete a blog post by its primary key (pk).
    - Returns: 204 No Content.
    """

    serializer_class = PostSerializer
    model = Post
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ["title", "auther"]
    search_filters = ["title", "content"]
    ordering_fields = "title"
    pagination_class = DefaultPagination

    def list(self, request):
        post_obj = self.model.objects.all()
        serializer = self.serializer_class(
            post_obj, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        instance = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(
            instance=instance, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(obj, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        instance = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(
            instance=instance,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListAndCreateAPIView(GenericAPIView):
    """
    API view for listing and creating comments associated with a specific post.

    Endpoints:
    - GET: Retrieve all published comments for the specified post.
    - POST: Create a new comment or a reply for the specified post.

    The authenticated user is automatically assigned as the comment owner.
    """
    serializer_class = CommentSerializer

    def get(self, request, pk):
        """
        Retrieve all published comments for the given post.

        Args:
            request (Request): Incoming HTTP request.
            pk (int): Primary key of the target post.

        Returns:
            Response: A list of serialized published comments.
        """
        comments = Comments.objects.filter(post__pk=pk, published=True)
        serializer = self.serializer_class(
            instance=comments, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        """
        Create a new comment or reply for the given post.

        The target post is determined by the URL parameter, while the
        authenticated user is assigned automatically by the serializer.
        If a `parent` field is provided, the comment is created as a reply.

        Args:
            request (Request): Incoming HTTP request containing comment data.
            pk (int): Primary key of the target post.

        Returns:
            Response: Success message on creation or validation errors.
        """
        data = request.data
        post = Post.objects.get(pk=pk)
        if not post:
            return Response({"message": "cant find any post with id you send"})

        serializer = self.serializer_class(data=data, context={"request": request,"post":post})
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(
                {"message": "comment successfuly added"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class CommentDetailAndDeleteAPIView(GenericAPIView):
    """
    API view for updating and deleting a specific comment.

    Endpoints:
    - PUT: Update an existing comment.
    - DELETE: Remove a comment from the database.
    """
    serializer_class = CommentDetailSerializer

    def put(self, request, pk):
        """
        Update the specified comment.

        Args:
            request (Request): Incoming HTTP request containing updated comment data.
            pk (int): Primary key of the target comment.

        Returns:
            Response: Success message on update or validation errors.
        """
        obj = Comments.objects.get(pk=pk)
        serializer = self.serializer_class(instance=obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "comment successfully updated"}, status=status.HTTP_200_OK
            )

        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        """
        Delete the specified comment.

        Args:
            request (Request): Incoming HTTP request.
            pk (int): Primary key of the target comment.

        Returns:
            Response: Success message if the comment is deleted, otherwise an
            error response if the comment does not exist.
        """
        obj = obj = Comments.objects.get(pk=pk)
        if obj:
            obj.delete()
            return Response(
                {"msg": "comment successfully deleted"},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"msg": "cant find any comment with this id "},
                status=status.HTTP_404_NOT_FOUND,
            )


class UserPostListApiView(GenericAPIView):
    """
    API view for retrieving posts created by the authenticated user.

    Endpoint:
    - GET: Return a list of all posts owned by the current authenticated user.
    """
    serializer_class = PostSerializer

    def get(self, request):
        """
        Retrieve all posts created by the authenticated user.

        Args:
            request (Request): Incoming HTTP request.

        Returns:
            Response: A list of serialized posts belonging to the current user.
        """
        obj = Post.objects.filter(auther=request.user)
        serializer = self.serializer_class(
            instance=obj, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostListCacheAPIView(GenericAPIView):
    """
    Cached Random Posts API

    Provides a cached collection of randomly selected posts
    to reduce database load and improve response times for
    frequently accessed content sections such as:

        - Homepage featured posts
        - Recommended posts
        - Trending content blocks
        - Discover sections

    Behavior:
        1. Attempts to retrieve serialized post data from cache.
        2. If cache exists, returns cached data immediately.
        3. If cache is missing:
            - Randomly selects up to 6 posts from the database.
            - Preserves the randomized order.
            - Serializes the selected posts.
            - Stores the result in cache for future requests.
        4. Returns the serialized post collection.

    Cache:
        Key:
            post_list

        Timeout:
            20 minutes (1200 seconds)

    Methods:
        GET

    Success Responses:
        200 OK

        [
            {
                "id": 1,
                "title": "Example Post",
                "content": "...",
                "image": "...",
                "created_date": "..."
            }
        ]

    Edge Cases:
        - Returns an empty list when no posts exist.
        - Returns fewer than 6 posts when the database
          contains less than 6 records.

    Performance Notes:
        - Minimizes repetitive database queries through caching.
        - Suitable for high-traffic public endpoints.
        - Randomization occurs only when cache is regenerated.
    """

    serializer_class = PostSerializer

    def get(self, request):
        cache_kay = "post_list"
        cache_data = cache.get(cache_kay)
        if cache_data:
            return Response(cache_data)
        ids = list(Post.objects.values_list("id", flat=True))
        selected_ids = random.sample(ids, k=min(6, len(ids)))
        posts = list(Post.objects.filter(id__in=selected_ids))
        posts.sort(key=lambda x: selected_ids.index(x.id))

        if not posts:
            return Response([])

        serializer = self.serializer_class(posts, many=True, context={"request": request})
        data = serializer.data
        cache.set(cache_kay, data, timeout=60 * 20)
        return Response(data)


class PostImageCreateAndListAPIView(GenericAPIView):
    """
    Post Image Management API

    This endpoint provides functionality for managing
    additional images related to a user's post.

    Features:
    - List all images belonging to a specific post.
    - Upload new images to an existing post.
    - Restrict access to the post owner.

    Supported Methods:
        GET:
            Retrieve all images attached to the target post.

        POST:
            Upload and attach a new image to the target post.

    Authentication:
        JWT Authentication required.

    Authorization:
        Only the owner of the post can access or modify
        its associated images.

    URL Parameters:
        pk (int):
            Primary key of the target post.

    Request Content-Type:
        multipart/form-data

    Success Responses:
        200 OK
        201 CREATED

    Error Responses:
        400 BAD REQUEST
        401 UNAUTHORIZED
        403 FORBIDDEN
        404 NOT FOUND
    """

    serializer_class = PostImagesSerializers

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk, author=request.user)
        images = PostImages.objects.filter(post=post)
        serializer = self.serializer_class(instance=images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        post = Post.objects.get(pk=pk, auther=request.user)
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            serializers.save(post=post)
            return Response(
                {"msg": "images successfully added"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializers.errors, status=status.HTTP_404_NOT_FOUND)

class SearchPostApiView(GenericAPIView):
    """
    Search posts using Elasticsearch.

    This endpoint performs a full-text search on the indexed `Post` documents
    based on the `title` field. It utilizes Elasticsearch's `multi_match`
    query with automatic fuzzy matching to handle misspellings and partial
    user input.

    Query Parameters:
        q (str): Search keyword.

    Returns:
        200 OK:
            A list of matching posts containing their `id` and `title`.

    Notes:
        - Uses Elasticsearch instead of querying the PostgreSQL database.
        - Fuzziness is set to `AUTO` to improve search accuracy.
    """
    serializer_class = SearchPostSerializer
    
    
    def get(self,request,*args,**kwargs):
        query = request.query_params.get('q','')
        search = PostDocument.search()
        if query:
            search = search.query(
                'multi_match',
                query = query,
                fields = [
                    'title'
                ],
                fuzziness = "AUTO"
            )
            response = search.execute()
            results = [ 
                      {
                          "id":hit.id,
                          "title":hit.title
                      }
                      for hit in response
                      ]
            serializer = self.serializer_class(instance=results,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        