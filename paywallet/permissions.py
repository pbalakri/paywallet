from rest_framework.permissions import BasePermission


class IsSchoolAdmin(BasePermission):
    def has_permission(self, request, view):
        # Check if the user belongs to the "school_admin" group
        return request.user.groups.filter(name='School Admin').exists()


class IsGuardian(BasePermission):
    def has_permission(self, request, view):
        # Check if the user belongs to the "guardian" group
        return request.user.groups.filter(name='Guardian').exists()


class isVendor(BasePermission):
    def has_permission(self, request, view):
        # Check if the user belongs to the "vendor" group
        return request.user.groups.filter(name='Vendor Admin').exists() or request.user.groups.filter(name='Vendor Operator').exists()
