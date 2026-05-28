from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.user_profile.models import StudentProfile, TeacherProfile
from apps.user_profile.serializers import (
    StudentProfileSerializer,
    TeacherProfileSerializer,
)
from apps.users.permissions import IsRole


# === 老师简介视图 ===
# 多重继承 CreateAPIView + RetrieveUpdateAPIView：
#   POST → 创建（首次）或更新（再次）
#   GET  → 查看自己的简介
#   PUT  → 全量更新
class TeacherProfileView(CreateAPIView, RetrieveUpdateAPIView):
    serializer_class = TeacherProfileSerializer
    # IsRole('TEACHER')：实例化时传入角色，只有该角色可访问
    permission_classes = [IsAuthenticated, IsRole('TEACHER')]

    def get_object(self):
        """覆写：始终操作当前登录用户自己的简介，而非 URL 中的 id"""
        return TeacherProfile.objects.get(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """首次 POST 创建，再次 POST 更新（有则更新，无则创建）"""
        if TeacherProfile.objects.filter(user=request.user).exists():
            profile = self.get_object()
            # partial=True：允许部分字段更新（PATCH 语义）
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        return super().create(request, *args, **kwargs)


# === 学生简介视图 ===
# 结构与 TeacherProfileView 一致，仅模型和角色不同
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
