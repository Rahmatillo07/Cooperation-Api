from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            return request.method in SAFE_METHODS


class ChatPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or obj.to_user == request.user
