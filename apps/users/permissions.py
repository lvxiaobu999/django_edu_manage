from rest_framework.permissions import BasePermission


class IsApprovedAdmin(BasePermission):
    """已审核通过的管理员 —— 三重检查：已登录 + 角色是管理员 + 已审核"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'ADMIN'
            and request.user.is_approved
        )
