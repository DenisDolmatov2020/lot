import datetime
from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from tracker.models import Tracker
from tracker.serializers import TrackerSerializer


class TrackerView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def add_energy(self, energy):
        self.request.user.energy += energy
        self.request.user.save(update_fields=['energy'])

    def get(self, request):
        tracker, created = Tracker.objects.get_or_create(user=self.request.user)
        if not created:
            tomorrow = (datetime.date.today() - datetime.timedelta(days=1))
            if tracker.date <= tomorrow:
                created = True
                tracker.days_row = 1 if tracker.date < tomorrow else tracker.days_row + 1

            tracker.date = datetime.date.today()
        if created:
            self.add_energy(tracker.days_row)
            tracker.save()
        serializer = TrackerSerializer(data=tracker.__dict__)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
