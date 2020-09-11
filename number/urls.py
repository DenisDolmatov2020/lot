from django.urls import path
from number.views import NumberListUpdateView

urlpatterns = [
    path('<int:pk>/', NumberListUpdateView.as_view(), name='NumberListUpdateView'),
]
