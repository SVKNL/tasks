from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Task


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class TaskSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    executors = UserSerializer(many=True, read_only=True)
    watchers = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'author', 'assignee', 'board', 'column', 'sprint', 'group', 'executors', 'watchers']

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

    def validate(self, data):
        if data['status'] == 'done' and not data['assignee']:
            raise serializers.ValidationError("Assignee must be set if status is 'done'.")
        return data