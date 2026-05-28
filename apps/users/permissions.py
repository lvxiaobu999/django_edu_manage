from rest_framework.permissions import BasePermission


# === 权限类 ===
# 自定义权限需要继承 BasePermission 并重写 has_permission()。
# 返回 True = 允许访问，False = 拒绝（返回 403 Forbidden）。
#
# DRF 内置权限（IsAuthenticated, AllowAny, IsAdminUser 等）可以组合使用，
# 权限列表中的所有类都必须通过。


class IsApprovedAdmin(BasePermission):
    """已审核通过的管理员 —— 三重检查：已登录 + 角色是管理员 + 已审核"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'ADMIN'
            and request.user.is_approved
        )


class IsRole(BasePermission):
    """
    限定特定角色才能访问。

    用法：
        permission_classes = [IsAuthenticated, IsRole('STUDENT')]

    与 IsApprovedAdmin 的区别：
        IsRole 不检查审核状态，只检查角色。
        适用于注册后、审核前也能完善个人简介的场景。
    """

    # __init__ 接收构造函数参数，实现"同一个类，不同角色"的复用
    def __init__(self, role):
        self.role = role

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == self.role
        )

    # has_object_permission：针对单个对象的权限检查（如 GET /api/5/）
    # 这里复用 has_permission 的逻辑
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
