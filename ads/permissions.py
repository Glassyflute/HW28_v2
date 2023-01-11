from rest_framework.permissions import BasePermission


class IsSelectionOwner(BasePermission):
    message = "Вы не имеете прав на это действие с подборкой."

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class IsAdAuthorOrStaff(BasePermission):
    message = "Вы не имеете доступа к этому объявлению."

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author or request.user.role in ["moderator", "admin"]:
            return True
        return False

