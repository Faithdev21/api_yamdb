from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    """Проверка является ли пользователь администратором или суперюзером при изменении контента."""
    message: str = 'Изменение контента запрещено!'

    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS
                    or request.user and request.user.is_staff
                    or request.user.is_superuser)

    def has_object_permission(self, request, view, obj) -> bool:
        """Установка разрешения на уровне объекта изменять
        контент только с правами администратора или суперюзера."""
        return request.user.is_staff or request.user.is_superuser
