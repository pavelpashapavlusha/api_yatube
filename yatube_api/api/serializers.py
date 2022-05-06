from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Group, Post, User


class UserSerializer(serializers.ModelSerializer):
    Post = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = fields = ('id', 'username', 'first_name', 'last_name',
                           'posts')
        ref_name = 'ReadOnlyUsers'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'created')
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')

    validators = [UniqueTogetherValidator(queryset=Group.objects.all(),
                                          fields=('slug',))]


class PostSerializer(serializers.ModelSerializer):
    group = GroupSerializer(many=False, required=False)
    image = serializers.ImageField(required=False)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ('id', 'text', 'image', 'author', 'pub_date', 'group')
