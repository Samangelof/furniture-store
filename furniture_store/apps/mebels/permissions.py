from rest_framework.permissions import BasePermission, IsAdminUser


class IsOwner(BasePermission):
    """
    Разрешение только владельцу объекта
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user
    

class AdminOnlyCreate(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return IsAdminUser().has_permission(request, view)
    


class IsOrderItemOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.order.user == request.user