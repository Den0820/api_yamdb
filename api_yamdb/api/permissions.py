from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    '''Разрешение создания, изменения и удаления только админу.'''

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.user.role == 'admin')
