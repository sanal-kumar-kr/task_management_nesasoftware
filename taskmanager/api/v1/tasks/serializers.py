from rest_framework import serializers
from tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['completion_report', 'worked_hours']

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']
    def validate(self, data):
        if data.get('status') == 'completed':
            if not data.get('completion_report') or not data.get('worked_hours'):
                raise serializers.ValidationError(
                    "Completion report and worked hours required when marking completed."
                )
        return data
