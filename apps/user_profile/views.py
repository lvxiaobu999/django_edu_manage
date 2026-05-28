from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.user_profile.models import ResearchGroup, StudentProfile, TeacherProfile
from apps.user_profile.serializers import (
    ResearchGroupSerializer,
    StudentProfileSerializer,
    TeacherProfileSerializer,
)
from apps.users.permissions import IsRole


# === 老师简介视图 ===
# 多重继承：CreateAPIView + RetrieveUpdateAPIView
#   CreateAPIView → 提供 POST（创建）
#   RetrieveUpdateAPIView → 提供 GET（查看）和 PUT/PATCH（更新）
# 三个独立类组合在一起，一个 URL 同时支持 POST/GET/PUT
#
# 实际上，下面的 create() 做了"有则更新，无则创建"的逻辑，
# 所以 POST /api/profile/teacher/ 首次创建，再次 POST 就是更新。
class TeacherProfileView(CreateAPIView, RetrieveUpdateAPIView):
    serializer_class = TeacherProfileSerializer
    # IsRole('TEACHER')：实例化权限类，传入构造函数参数 'TEACHER'
    # 只有 role='TEACHER' 的用户才能访问
    permission_classes = [IsAuthenticated, IsRole('TEACHER')]

    def get_object(self):
        # 覆写 get_object：检索当前登录用户自己的简介
        # 这样 GET 和 PUT 操作的就是"我自己的简介"，而不是任意用户的
        return TeacherProfile.objects.get(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # 逻辑：如果已存在简介 → 更新；不存在 → 创建
        # 这样 POST 接口同时承担了"完善"和"修改"两个功能
        if TeacherProfile.objects.filter(user=request.user).exists():
            profile = self.get_object()
            # partial=True：允许部分字段更新（PATCH 语义）
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        return super().create(request, *args, **kwargs)


# === 学生简介视图 ===
# 结构与 TeacherProfileView 完全一致，仅模型和权限角色不同
class StudentProfileView(CreateAPIView, RetrieveUpdateAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated, IsRole('STUDENT')]

    def get_object(self):
        return StudentProfile.objects.get(user=self.request.user)

    def create(self, request, *args, **kwargs):
        if StudentProfile.objects.filter(user=request.user).exists():
            profile = self.get_object()
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        return super().create(request, *args, **kwargs)


# === 教研组 ViewSet ===
# 标准 CRUD，IsAuthenticated 表示只需要登录即可访问
class ResearchGroupViewSet(viewsets.ModelViewSet):
    queryset = ResearchGroup.objects.all()
    serializer_class = ResearchGroupSerializer
    permission_classes = [IsAuthenticated]
