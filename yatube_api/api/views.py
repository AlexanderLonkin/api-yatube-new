from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from posts.models import Group, Post

from .permissions import IsAuthenticatedAndAuthorOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(ModelViewSet):
    """Читает и создаёт посты, даёт автору менять и удалять свои посты."""

    queryset = Post.objects.select_related('author')
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedAndAuthorOrReadOnly,)
    lookup_url_kwarg = 'post_id'
    lookup_value_regex = r'\d+'

    def perform_create(self, serializer):
        """Назначает текущего пользователя автором нового поста."""
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    """Возвращает список групп или данные одной группы."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_url_kwarg = 'group_id'
    lookup_value_regex = r'\d+'


class CommentViewSet(ModelViewSet):
    """Обрабатывает запросы к комментариям конкретного поста."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedAndAuthorOrReadOnly,)
    lookup_url_kwarg = 'comment_id'
    lookup_value_regex = r'\d+'

    def get_post(self):
        """Возвращает пост по `post_id` из URL или возбуждает `Http404`."""
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_queryset(self):
        """Ограничивает выборку комментариями поста из URL."""
        return self.get_post().comments.select_related('author')

    def perform_create(self, serializer):
        """Связывает комментарий с текущим пользователем и постом из URL."""
        serializer.save(author=self.request.user, post=self.get_post())
