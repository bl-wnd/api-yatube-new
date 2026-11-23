from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


class AuthorPermissionMixin():
    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionDenied('Редактирование чужих записей запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied('Удаление чужих записей запрещено!')
        super().perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(AuthorPermissionMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(AuthorPermissionMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)
