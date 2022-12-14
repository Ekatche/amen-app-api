from rest_framework import permissions

from .models import ROLE_DEV, ROLE_ADMIN, ROLE_SALES


class BackofficePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and (request.user.amen_role is not None):
            return True
        elif not request.user.is_authenticated:
            self.message = f"user is authenticated {request.user.is_authenticated}"
        else:
            self.message = "You do not have a role in this organozation"

        return False


class NoDevBackofficePermission(BackofficePermission):
    def has_permission(self, request, view):
        return not request.user.amen_role == ROLE_DEV


class NoAdminBackofficePermission(BackofficePermission):
    def has_permission(self, request, view):
        return not request.user.amen_role == ROLE_ADMIN


class NoSalesBackofficePermission(BackofficePermission):
    def has_permission(self, request, view):
        return not request.user.amen_role == ROLE_SALES


class ReadOnlyDevBackofficePermission(BackofficePermission):
    def has_permission(self, request, view):
        return not (
            request.method not in permissions.SAFE_METHODS
            and request.user.amen_role == ROLE_DEV
        )


class ReadOnlyAdminBackofficePermission(BackofficePermission):
    def has_permission(self, request, view):
        return not (
            request.method not in permissions.SAFE_METHODS
            and request.user.amen_role == ROLE_ADMIN
        )


class ReadOnlySalesBackofficePermission(BackofficePermission):
    def has_permission(self, request, view):
        return not (
            request.method not in permissions.SAFE_METHODS
            and request.user.amen_role == ROLE_SALES
        )


class ReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthenticatedAndReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return not (
            request.method not in permissions.SAFE_METHODS
            and request.user.is_authenticated
        )
