from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission): #custom permission 
    message = "You Must be owner of this object(User Who created it)"

    def has_object_permission(self, request ,view, obj):
        if request.method == 'GET':
            return True
        return obj.user == request.user
