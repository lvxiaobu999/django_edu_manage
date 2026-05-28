from rest_framework.permissions import BasePermission


class IsApprovedAdmin(BasePermission):
    """已审核通过的管理员"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'ADMIN'
            and request.user.is_approved
        )


class IsRole(BasePermission):
    """指定角色的用户"""

    def __init__(self, role):
        self.role = role

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == self.role
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
