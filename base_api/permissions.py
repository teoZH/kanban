from rest_framework import permissions



class IsOwnerOrReadOnlyUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.creator == request.user


class IsOwnerOrReadOnlyObject(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class IsOwnerOrReadOnlyTodo(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ["DELETE"]:
            if obj.company:
                return obj.company.creator == request.user
        return obj.user == request.user


#request user if owner of company can change everything
#request user if not owner of company can change only in progress