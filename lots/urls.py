from django.urls import path
from rest_framework.routers import DefaultRouter
from lots.views import LotViewSet, NumberListUpdateView, TimelinesList, WinnersList

urlpatterns = [
    path('number/<int:pk>/', NumberListUpdateView.as_view(), name='NumberListUpdateView'),
    path('timelines/', TimelinesList.as_view(), name='TimelinesListView'),
    path('winners/<int:pk>/', WinnersList.as_view(), name='WinnersListView'),
]

router = DefaultRouter()
router.register(r'', LotViewSet, basename='lots')
urlpatterns += router.urls
