from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.classes.models import Classes
from apps.classes.serializers import ClassesSerializer


class ClassesViewSet(viewsets.ModelViewSet):
    queryset = Classes.objects.select_related('headmaster__user')
    serializer_class = ClassesSerializer
    permission_classes = [IsAuthenticated]
