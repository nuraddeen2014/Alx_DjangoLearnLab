from rest_framework.permissions import BasePermission


class OnlyOwnerDeletesPermission(BasePermission):
    """Ensures only the author of the post or comment deletes or edits it"""
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.author == request.user
        elif request.method in ['POST', 'GET', 'HEAD', 'OPTIONS']:
            return True