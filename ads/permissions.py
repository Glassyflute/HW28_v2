from rest_framework.permissions import BasePermission


class IsSelectionOwner(BasePermission):
    message = "Вы не имеете прав на это действие."

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False

