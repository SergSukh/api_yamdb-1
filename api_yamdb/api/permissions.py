from rest_framework.permissions import BasePermission, SAFE_METHODS

MODERATOR = ['admin', 'moderator']


class IsAdminOrReadOnly(BasePermission):
    """Разрешение на уровне админ."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.role == 'admin'
        else:
            False


class CustomIsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'admin'
        else:
            False


class ModeratorOrReadOnly(BasePermission):
    """Разрешение на уровне модератор."""
    def has_permission(self, request, view):
        """Безопасный метод или роль пользователя выше чем user."""
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.user.role in MODERATOR:
                return True
        else:
            return False


class AuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.user.role in MODERATOR:
                return True
        else:
            return obj.author == request.user
