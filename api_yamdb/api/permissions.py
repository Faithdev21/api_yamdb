from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminModeratorAuthorPermission(BasePermission):
    """Permissions to admins, moderators, authors."""

    def has_permission(self, request, view) -> bool:
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj) -> bool:
        return (request.method in SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)


class IsAdmin(BasePermission):
    """Permissions to admins."""
    def has_permission(self, request, view) -> bool:
        return (request.user.is_superuser
                or (request.user.is_authenticated and request.user.is_admin))


class IsAdminOrReadOnly(BasePermission):
    """Permissions to admins or read only."""

    def has_permission(self, request, view) -> bool:
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )
