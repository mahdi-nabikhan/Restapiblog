from rest_framework import serializers

from blog.models import Post, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('auther',)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['auther'] = request.user
        return Post.objects.create(**validated_data)

    def to_representation(self, instance):
        result = super(PostSerializer, self).to_representation(instance)
        result['category'] = CategorySerializer(instance.category).data
        return result


