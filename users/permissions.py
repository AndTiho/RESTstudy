from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Разрешает доступ только владельцу объекта.
    Используется для проверки права на изменение/удаление.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsModer(permissions.BasePermission):
    """
    Разрешает доступ пользователям из группы 'moders'.
    Проверяет наличие группы на уровне запроса (не объекта).
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()

    def has_object_permission(self, request, view, obj):
        # Для согласованности: модератор может работать с любым объектом
        return self.has_permission(request, view)


class IsNotModerator(permissions.BasePermission):
    """
    Запрещает доступ пользователям из группы 'moders'.
    Используется, чтобы исключить модераторов из определённых действий.
    """

    def has_permission(self, request, view):
        return not request.user.groups.filter(name="moders").exists()


class IsOwnerOrModerator(permissions.BasePermission):
    """
    Разрешает доступ:
    - владельцу объекта,
    - пользователю из группы 'moders'.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # 1. Владелец объекта
        if obj.owner == user:
            return True

        # 2. Модератор
        if user.groups.filter(name="moders").exists():
            return True

        return False
