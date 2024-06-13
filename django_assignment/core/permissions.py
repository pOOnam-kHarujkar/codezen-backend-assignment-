# permissions.py

from rest_framework import permissions

class IsCustomerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only customers to edit their own orders.
    """

    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, or OPTIONS requests (read-only) for any user
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow customers to edit their own orders
        return obj.customer == request.user.customer


class IsSellerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only sellers to edit their own products.
    """

    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, or OPTIONS requests (read-only) for any user
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow sellers to edit their own products
        return obj.seller == request.user.seller
