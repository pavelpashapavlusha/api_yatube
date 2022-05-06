from rest_framework import serializers

from posts.models import Comment, Group, Post, User


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text', 'author', 'post', 'created',)


class PostSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(
        slug_field='slug', queryset=Group.objects.all()
    )
    comment = CommentSerializer(required=False, many=True)

    class Meta:
        model = Post
        fields = (
            'id', 'text', 'author', 'image', 'pub_date', 'group', 'comment',
        )
        read_only_fields = ('author',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('title', 'slug', 'description',)
        read_only_field = ('slug',)


class UserSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'cats')
        ref_name = 'ReadOnlyUsers'
