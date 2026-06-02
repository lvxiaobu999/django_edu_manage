from rest_framework.permissions import BasePermission


class IsApprovedAdmin(BasePermission):
    """已审核通过的管理员 —— 三重检查：已登录 + 角色是管理员 + 已审核"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'ADMIN'
            and request.user.is_approved
        )


def IsRole(role):
    """工厂函数，返回一个限定特定角色的权限类。

    DRF 的 permission_classes 列表期望的是类（会被 get_permissions() 实例化），
    而不能是已实例化的对象。所以这里用工厂函数返回一个类，用法不变：

        permission_classes = [IsAuthenticated, IsRole('TEACHER')]
        permission_classes = [IsAuthenticated, IsRole('STUDENT')]

    与 IsApprovedAdmin 的区别：
        IsRole 不检查审核状态，只检查角色。
        适用于注册后、审核前也能完善个人简介的场景。
    """

    class _IsRole(BasePermission):
        def has_permission(self, request, view):
            return (
                request.user.is_authenticated
                and request.user.role == role
            )

        def has_object_permission(self, request, view, obj):
            return self.has_permission(request, view)

    return _IsRole
