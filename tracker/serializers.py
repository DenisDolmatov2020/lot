from rest_framework import serializers
from tracker.models import Tracker


class TrackerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tracker
        fields = ['days_row']
