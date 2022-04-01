from rest_framework import permissions


class IsModeratorOrReadOnly(permissions.BasePermission):
    """Разрешение на уровне модератор."""

    def has_object_permission(self, request, view, obj):
        """Безопасный метод или роль пользователя выше чем user"""
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.roles != 'user':
            return True
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение на уровне админ."""

    def has_object_permission(self, request, view, obj):
        """Безопасный метод или роль пользователя админ"""
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.roles == 'admin':
            return True
        return False
