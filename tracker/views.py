import datetime
import math
from collections import namedtuple
# Create your views here.
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from lots.models import Lot, LotNumber, Condition
from my_user.models import User
from tracker.models import Tracker
from tracker.serializers import TrackerSerializer


class TrackerView(APIView):
    permission_classes = [IsAuthenticated]

    def add_energy(self):
        user = User.objects.get(id=self.request.user.id)
        user.energy += user.level
        user.save()

    def add_star(self, tracker):
        user = User.objects.get(id=self.request.user.id)
        user.stars += math.ceil(user.level / 10)
        if tracker.days_row >= 2 + user.level and \
           tracker.days_all >= 5 + (2 * user.level) and \
           tracker.level_minutes >= 120 * (3 + user.level):
            user.level += 1
            tracker.level_minutes = 0
            tracker.days_row = 1
            tracker.days_all = 1
            tracker.save()
        user.save()

    def add_time(self, tracker):
        tracker.now_success = False
        if tracker.created:
            tracker.now_minutes = 5
            tracker.day_minutes = 5

            last = Tracker.objects.filter(user=self.request.user).latest('time')
            tracker.level_minutes = last.level_minutes + last.day_minutes
            tracker.days_all = last.days_all + 1
            if (tracker.date - last.date).days == 1:
                tracker.days_row = last.days_row + 1
                if tracker.days_row == 2 + self.request.user.level:
                    self.add_star(tracker)
                if tracker.days_all == 5 + (2 * self.request.user.level):
                    self.add_star(tracker)
            else:
                tracker.days_row = 1
        else:
            now = timezone.now()
            timedelta = (now - tracker.time).seconds
            if timedelta > 3:
                tracker.day_minutes += 5
                if timedelta < 10:
                    tracker.now_minutes += 5
                    if tracker.now_minutes == 15 * (2 + self.request.user.level) and not tracker.now_ready:
                        self.add_energy()
                        tracker.now_ready = True
                        tracker.now_success = True
                else:
                    tracker.now_minutes = 5
            else:
                return Response(status=status.HTTP_408_REQUEST_TIMEOUT)

        if tracker.level_minutes + tracker.day_minutes == 120 * (3 + self.request.user.level):
            self.add_star(tracker)
            if tracker.day_minutes == 20 * (5 + self.request.user.level):
                self.add_energy()

    def get(self, request):
        tracker, tracker.created = Tracker.objects.get_or_create(date=datetime.date.today(), user=self.request.user)
        self.add_time(tracker)
        tracker.time = timezone.now()
        tracker.save()
        serializer = TrackerSerializer(data=tracker.__dict__)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)