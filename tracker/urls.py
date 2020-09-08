from django.urls import path
from tracker.views import TrackerView

urlpatterns = [
    path('', TrackerView.as_view(), name='tracker-view'),
]
