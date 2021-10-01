from rest_framework import permissions


class CustomPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in 'list':
            return True
        else:
            return bool(request.user and request.user.is_authenticated)
