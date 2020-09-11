from django.urls import path
from rest_framework.routers import DefaultRouter
from lots.views import LotViewSet, TimelinesList

urlpatterns = [
    path('timelines/', TimelinesList.as_view(), name='TimelinesListView'),
]

router = DefaultRouter()
router.register(r'', LotViewSet, basename='lots')
urlpatterns += router.urls
