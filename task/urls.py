from task.views import TasksView
from django.urls import path

urlpatterns = [
    path('', TasksView.as_view()),
]

