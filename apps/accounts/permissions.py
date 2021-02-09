from rest_framework.permissions import BasePermission

from apps.accounts.models import User

from rest_framework import permissions


class IsOpuOnly(BasePermission):
    def has_permission(self, request, view):
        return True if request.user.subdepartment.id == 1 else False

class IsCreator(BasePermission):
    def has_permission(self, request, view):
        return True if view.get_object().user.user.pk == request.user.pk else False
