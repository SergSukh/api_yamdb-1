from rest_framework.permissions import BasePermission, SAFE_METHODS

MODERATOR = ['admin', 'moderator']


class IsAdminOrReadOnly(BasePermission):
    """Разрешение на уровне админ."""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == 'admin'


class CustomIsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'


class IsModeratorOrReadOnly(BasePermission):
    """Разрешение на уровне модератор."""
    def has_object_permission(self, request, view, obj):
        """Безопасный метод или роль пользователя выше чем user."""
        if request.method in SAFE_METHODS:
            return True
        if request.user.role in MODERATOR:
            return True
        return False
