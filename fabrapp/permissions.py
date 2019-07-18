from rest_framework.permissions import BasePermission


class IsFabricator(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "fabricator"
