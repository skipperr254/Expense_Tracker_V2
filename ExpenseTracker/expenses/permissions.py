from rest_framework import permissions

# Custom permission class to allow read-only access to all users and write access to admins.
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Check if the user has permission for the requested action.

        - Read-only access is allowed for all users.
        - Write access is restricted to admins.

        Args:
            request: The HTTP request object.
            view: The view object where this permission is used.

        Returns:
            bool: True if the user has permission; False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

# Custom permission class to allow read-only access to all users and write access to the owner.
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission for the requested action on an object.

        - Read-only access is allowed for all users.
        - Write access is restricted to the owner of the object.

        Args:
            request: The HTTP request object.
            view: The view object where this permission is used.
            obj: The object being accessed.

        Returns:
            bool: True if the user has permission; False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
