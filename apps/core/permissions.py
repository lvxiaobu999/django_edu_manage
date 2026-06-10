from rest_framework.permissions import BasePermission


def IsRole(role):
    """工厂函数，返回一个限定特定角色的权限类。

    DRF 的 permission_classes 列表期望的是类（会被 get_permissions() 实例化），
    而不能是已实例化的对象。所以这里用工厂函数返回一个类，用法不变：

        permission_classes = [IsAuthenticated, IsRole('TEACHER')]
        permission_classes = [IsAuthenticated, IsRole('STUDENT')]

    不检查审核状态，只检查角色。
    适用于注册后、审核前也能完善个人简介的场景。
    """

    class _IsRole(BasePermission):
        def has_permission(self, request, view):
            # 兼容单角色字符串和多角色列表/元组
            allowed = role if isinstance(role, (list, tuple)) else [role]
            return request.user.is_authenticated and request.user.role in allowed

        def has_object_permission(self, request, view, obj):
            return self.has_permission(request, view)

    return _IsRole
