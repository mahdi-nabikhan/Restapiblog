from rest_framework import serializers

from blog.models import Post, Category


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
        fields = '__all__'


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
    snippet = serializers.ReadOnlyField(source='get_snippet')
    relative_url = serializers.URLField(source='get_absolute_api_url', read_only=True)
    absolute_url = serializers.SerializerMethodField(source='get_absolute_url')

    class Meta:
        model = Post
        fields = ['title', 'content', 'auther', 'snippet', 'status', 'created_date', 'relative_url']
        read_only_fields = ('auther',)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['auther'] = request.user
        return Post.objects.create(**validated_data)

    def to_representation(self, instance):
        result = super(PostSerializer, self).to_representation(instance)
        result['category'] = CategorySerializer(instance.category).data
        return result

    def get_absolute_url(self, instance):
        request = self.context.get('request')
        return request.build_absolute_uri(instance.get_absolute_url())
