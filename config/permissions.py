from rest_framework.permissions import BasePermission

__all__ = ["IsAuthenticated", "AllowAny"]


class AllowAny(BasePermission):
    def has_permission(self, request, view):
        return True


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_active and request.user.is_authenticated
        )
