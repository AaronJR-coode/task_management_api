from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwner

# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['status', 'priority', 'due_date']
    ordering_fields = ['due_date', 'priority', 'created_at']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user).order_by('due_date')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwner]
        return [perm() for perm in permission_classes]

    @action(detail=True, methods=['post'], url_path='mark-complete')
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        if task.status == Task.STATUS_COMPLETED:
            return Response({"detail": "Task already completed."}, status=status.HTTP_400_BAD_REQUEST)
        task.mark_complete()
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='mark-incomplete')
    def mark_incomplete(self, request, pk=None):
        task = self.get_object()
        if task.status == Task.STATUS_PENDING:
            return Response({"detail": "Task already pending/incomplete."}, status=status.HTTP_400_BAD_REQUEST)
        task.mark_incomplete()
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)