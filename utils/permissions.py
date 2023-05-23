from rest_framework.permissions import SAFE_METHODS, BasePermission

class SafeMethodsOnly(BasePermission):
    """
    Only read methods are allowed.
    """

    def has_permission(self, request, view) -> bool:
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj) -> bool:
        return self.has_permission(request, view)




class IsAdminOrReadAndUpdate(SafeMethodsOnly):
    """
    Admin has all permissions, others post only.
    """

    def has_permission(self, request, view) -> bool:
        return (
            request.method in SAFE_METHODS
            or request.method in ["PATCH", "PUT"]
            or (request.user and request.user.is_staff)
        )