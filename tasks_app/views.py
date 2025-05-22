from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination

from .models import Task
from .serializers import TaskSerializer
import logging

logger = logging.getLogger(__name__)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['status', 'author__id', 'assignee__id', 'board__id', 'sprint__id']
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
            logger.info('Задача успешно создана')
        except Exception as e:
            logger.error('Ошибка при создании задачи: %s', e)

    def get_object(self):
        try:
            return get_object_or_404(Task, pk=self.kwargs['pk'])
        except Task.DoesNotExist:
            logger.error(f'Задача с ID {self.kwargs["pk"]} не найдена')
            raise ValidationError({'detail': 'Задача не найдена'})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                logger.info(f'Задача {instance.id} успешно обновлена')
                return serializer.data
        except Exception as e:
            logger.error(f'Ошибка при обновлении задачи {instance.id}: {e}')
            raise
        return super().update(request, *args, **kwargs)