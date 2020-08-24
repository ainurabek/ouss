from rest_framework.permissions import BasePermission

from apps.accounts.models import User

from rest_framework import permissions


class IsOpuOnly(BasePermission):
    def has_permission(self, request, view):
        users = User.objects.filter(subdepartment__id=1)
        print(users)
        for user in users:
            if user.subdepartment.id == request.user.subdepartment.id:
                return True
            else:
                return False


class IsCreator(BasePermission):
    def has_permission(self, request, view):
        return True if view.get_object().user.user.pk == request.user.pk else False
