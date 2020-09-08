from rest_framework import serializers
from tracker.models import Tracker
from my_user.serializers import UserSerializer


class TrackerSerializer(serializers.ModelSerializer):
    created = serializers.BooleanField()
    now_success = serializers.BooleanField()

    class Meta:
        model = Tracker
        fields = [
            'created',
            'now_ready',
            'now_success',
            'now_minutes',
            'day_minutes',
            'level_minutes',
            'days_row',
            'days_all'
        ]
