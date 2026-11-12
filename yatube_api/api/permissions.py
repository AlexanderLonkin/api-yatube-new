from rest_framework.permissions import SAFE_METHODS, IsAuthenticated


class IsAuthenticatedAndAuthorOrReadOnly(IsAuthenticated):
    """Разрешает чтение после входа, а изменение и удаление — автору."""

    def has_object_permission(self, request, view, obj):
        """Разрешает безопасный запрос или проверяет авторство объекта."""
        return (
            request.method in SAFE_METHODS or obj.author_id == request.user.pk
        )
