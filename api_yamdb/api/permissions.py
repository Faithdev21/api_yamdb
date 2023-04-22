from rest_framework import permissions


class AdminModeratorAuthorPermission(permissions.BasePermission):
    """Used to issue permissions to admins, moderators, authors."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)


class IsAdmin(permissions.BasePermission):
    """Used to issue permissions to admins."""
    def has_permission(self, request, view):
        return request.user.is_superuser or (request.user.is_authenticated and request.user.is_admin)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Used to issue permissions to admins or read only."""
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_admin
        )
