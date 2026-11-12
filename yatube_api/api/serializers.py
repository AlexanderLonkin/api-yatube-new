from rest_framework import serializers

from posts.models import Comment, Group, Post


class PostSerializer(serializers.ModelSerializer):
    """Представляет пост с именем пользователя в поле автора."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')


class GroupSerializer(serializers.ModelSerializer):
    """Представляет идентификатор, название, slug и описание группы."""

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    """Представляет комментарий с именем автора и идентификатором поста."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post',)
