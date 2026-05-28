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


class TeacherProfileView(CreateAPIView, RetrieveUpdateAPIView):
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAuthenticated, IsRole('TEACHER')]

    def get_object(self):
        return TeacherProfile.objects.get(user=self.request.user)

    def create(self, request, *args, **kwargs):
        if TeacherProfile.objects.filter(user=request.user).exists():
            profile = self.get_object()
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        return super().create(request, *args, **kwargs)


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


class ResearchGroupViewSet(viewsets.ModelViewSet):
    queryset = ResearchGroup.objects.all()
    serializer_class = ResearchGroupSerializer
    permission_classes = [IsAuthenticated]
