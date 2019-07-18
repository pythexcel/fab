from rest_framework.permissions import BasePermission


class IsExhibitor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "exhibitor"
