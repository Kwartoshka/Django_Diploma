from rest_framework.permissions import BasePermission


class IsAuthorOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or bool(request.user and request.user.is_staff)


class IsStatus(BasePermission):

    def has_object_permission(self, request, view, obj):
        status = request.data.get('status', None)
        if status:
            return bool(request.user and request.user.is_staff)
        else:
            return True
