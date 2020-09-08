from rest_framework import serializers
from task.models import Tasks


class TasksSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Tasks
        fields = ['user_id', 'level_time', 'day_time', 'now_time', 'word']
