from rest_framework.permissions import BasePermission


class IsSchoolAdmin(BasePermission):
    def has_permission(self, request, view):
        # Check if the user belongs to the "school_admin" group
        return request.user.groups.filter(name='School Admin').exists() or request.user.is_superuser


class IsGuardian(BasePermission):
    def has_permission(self, request, view):
        # Check if the user belongs to the "guardian" group
        return request.user.groups.filter(name='Guardian').exists() or request.user.is_superuser


class isVendor(BasePermission):
    def has_permission(self, request, view):
        # Check if the user belongs to the "vendor" group
        return request.user.groups.filter(name='Vendor Admin').exists() or request.user.is_superuser or request.user.groups.filter(name='Vendor Operator').exists()
