from rest_framework import serializers
from django.utils import timezone
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = [
            'id', 'owner', 'title', 'description', 'due_date',
            'priority', 'status', 'completed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'completed_at', 'created_at', 'updated_at']

    def validate_due_date(self, value):
        now = timezone.now()
        if value <= now:
            raise serializers.ValidationError("Due date must be in the future.")
        return value

    def validate_priority(self, value):
        allowed = [c[0] for c in Task.PRIORITY_CHOICES]
        if value not in allowed:
            raise serializers.ValidationError(f"Priority must be one of {allowed}.")
        return value

    def validate_status(self, value):
        allowed = [c[0] for c in Task.STATUS_CHOICES]
        if value not in allowed:
            raise serializers.ValidationError(f"Status must be one of {allowed}.")
        return value

    def update(self, instance, validated_data):
        if instance.status == Task.STATUS_COMPLETED:
            new_status = validated_data.get('status', instance.status)
            if new_status != Task.STATUS_PENDING:
                raise serializers.ValidationError("Completed tasks cannot be edited unless reverted to pending.")
        return super().update(instance, validated_data)
