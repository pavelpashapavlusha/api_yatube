from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets

from posts.models import Comment, Group, Post, User

from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, GroupSerializer,
                          PostSerializer, UserSerializer)


class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    pass


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_class = IsOwnerOrReadOnly

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets. ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_class = IsOwnerOrReadOnly

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post__id=post_id)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)
