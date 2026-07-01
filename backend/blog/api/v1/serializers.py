from rest_framework import serializers

from blog.models import Post, Category, Comments, PostImages


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.

    This serializer automatically maps all fields of the Category model
    using Django REST Framework's ModelSerializer.

    Features:
    - Serializes all fields defined in the Category model (`fields = '__all__'`)
    - Useful for both read and write operations (GET, POST, PUT, PATCH, DELETE)

    Example usage:
        serializer = CategorySerializer(category_instance)
        serialized_data = serializer.data

    Meta:
        model: Category
        fields: '__all__' (includes all model fields)
    """

    class Meta:
        model = Category
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.

    This serializer handles:
    - Automatic mapping of all model fields via ModelSerializer.
    - Setting the 'auther' field to the currently authenticated user during creation.
    - Custom representation of the 'category' field using a nested CategorySerializer.

    Meta:
        model: Post
        fields: '__all__'
            Includes all fields of the Post model.
        read_only_fields: ('auther',)
            Ensures 'auther' is not modifiable by the client; it is set automatically.

    Methods:
        create(validated_data):
            Sets the 'auther' field to the current authenticated user before creating a Post instance.

        to_representation(instance):
            Overrides default representation to include full serialized data of related 'category'
            using CategorySerializer instead of showing only its ID.

    Example:
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
    """

    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField(source="get_absolute_url")

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "auther",
            "snippet",
            "status",
            "created_date",
            "relative_url",
            "absolute_url",
            "image",
        ]
        read_only_fields = ("auther",)

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["auther"] = request.user
        return Post.objects.create(**validated_data)

    def to_representation(self, instance):
        request = self.context.get("request")
        result = super(PostSerializer, self).to_representation(instance)
        if request.parser_context.get("kwargs").get("pk"):
            result.pop("snippet")
            result.pop("absolute_url")
            result.pop("relative_url")
        else:
            result.pop("content")
        result["category"] = CategorySerializer(instance.category).data
        return result

    def get_absolute_url(self, instance):
        request = self.context.get("request")
        return request.build_absolute_uri(instance.pk)


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and representing comment objects.

    Automatically associates the authenticated user with newly created
    comments and provides a nested representation of the parent comment.
    """
    class Meta:
        model = Comments
        fields = [
            "pk",
            "user",
            "post",
            "content",
            "created_at",
            "published",
            "updated_at",
            "parent"
        ]
        read_only_fields = ("user", "post")

    def create(self, validated_data):
        """
        Create a new comment and assign the authenticated user as its owner.

        Args:
            validated_data (dict): Validated serializer data.

        Returns:
            Comments: The newly created comment instance.
        """
        request = self.context.get("request")
        validated_data["user"] = request.user

        return Comments.objects.create(**validated_data)
    
    def to_representation(self, instance):
        """
        Customize the serialized representation of a comment.

        Replaces the parent comment primary key with a nested serialized
        representation. Returns `None` when the comment has no parent.

        Args:
            instance (Comments): Comment instance to serialize.

        Returns:
            dict: Serialized comment data.
        """
        result = result = super().to_representation(instance)
        if instance.parent:
            result["parent"] = CommentDetailSerializer(instance.parent).data
        else:
            result["parent"] = None

        return result
    
    def validate_parent(self, value):
        if value is None:
            return value

        post = self.context["post"]

        if value.post != post:
         raise serializers.ValidationError(
                "You cannot reply to a comment from another post."
            )

        return value
class CommentDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for representing a comment along with its parent comment.

    Produces a recursive nested representation of the parent comment,
    allowing clients to traverse the comment thread hierarchy.
    """
    class Meta:
        model = Comments
        fields = ["content","parent"]
        
    def to_representation(self, instance):
        """
        Return a serialized representation of the comment.

        Replaces the parent comment primary key with its serialized
        representation. If the comment has no parent, the `parent`
        field is set to ``None``.

        Args:
            instance (Comments): The comment instance to serialize.

        Returns:
            dict: Serialized comment data.
        """
        result = result = super().to_representation(instance)
        if instance.parent:
            result["parent"] = CommentDetailSerializer(instance.parent).data
        else:
            result["parent"] = None

        return result
        


class PostImagesSerializers(serializers.ModelSerializer):
    """
    Serializer for managing post image objects.

    Serializes all fields of the PostImages model while preventing direct
    modification of the associated post. The `post` field is read-only and
    is intended to be assigned automatically by the corresponding view.
    """
    class Meta:
        model = PostImages
        fields = "__all__"
        read_only_fields = ("post",)







class SearchPostSerializer(serializers.Serializer):
    """
    Serializer for Elasticsearch search results.

    Represents the minimal post information returned by the search endpoint,
    including the post identifier and title.
    """
    
    id = serializers.IntegerField()
    title = serializers.CharField()