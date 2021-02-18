from rest_framework.permissions import BasePermission

from apps.accounts.models import User

from rest_framework import permissions


class IsPervichkaOnly(BasePermission):
    def has_permission(self, request, view):
        return True if request.user.subdepartment.id == 1 else False

class IsVtorichkaOnly(BasePermission):
    def has_permission(self, request, view):
        return True if request.user.subdepartment.id == 2 else False

class IsDispOnly(BasePermission):
    def has_permission(self, request, view):
        return True if request.user.subdepartment.id == 3 else False

class IsAKOnly(BasePermission):
    def has_permission(self, request, view):
        return True if request.user.subdepartment.id == 4 else False

class IsCreator(BasePermission):
    def has_permission(self, request, view):
        return True if view.get_object().user.user.pk == request.user.pk else False

class SuperUser(BasePermission):
    def has_permission(self, request, view):
        return True if request.user.role.id == 1 else False

class IngenerUser(BasePermission):
    def has_permission(self, request, view):
        return True if request.user.role.id == 2else False

class IsReadOnlyUser(BasePermission):
    def has_permission(self, request, view):
        return True if request.user.role.id == 3 else False