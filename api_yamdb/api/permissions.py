from rest_framework import permissions
from users.models import CustomUser
from django.shortcuts import get_object_or_404


class AdminRole(permissions.BasePermission):

    def has_permission(self, request, view):
        cur_user = get_object_or_404(CustomUser, username=request.user.username)
        return (
            cur_user.is_admin
        )
 