from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .serializers import *
from blog.models import *
from rest_framework.viewsets import ViewSet
from .permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import DefaultPagination


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
    filterset_fields = ['title', 'auther']
    search_fields = ['title', 'content']
    ordering_fields = 'title'
    pagination_class = DefaultPagination
    queryset = Post.objects.all()

    def get(self, request):
        post_obj =self.get_queryset()
        serializer = self.serializer_class(post_obj, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data, context={'request': request})
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
    filterset_fields = ['title', 'auther']
    ordering_fields = 'title'
    queryset = Post.objects.all()

    def get(self, request, pk):
        post_obj = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(post_obj, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post_obj = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(instance=post_obj, data=request.data, context={'request': request})
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
        serializer = self.serializer_class(instance=self.model.objects.get(pk=pk), data=request.data, partial=True,
                                           context={'request': request})
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
    filterset_fields = ['title', 'auther']
    search_filters = ['title', 'content']
    ordering_fields = 'title'
    pagination_class = DefaultPagination

    def list(self, request):
        post_obj = self.model.objects.all()
        serializer = self.serializer_class(post_obj, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        instance = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(instance=instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(obj, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        instance = self.model.objects.get(pk=pk)
        serializer = self.serializer_class(instance=instance, data=request.data, partial=True,
                                           context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
