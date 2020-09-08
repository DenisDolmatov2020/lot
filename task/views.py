from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from my_user.models import User
from task.models import Tasks
from task.serializer import TasksSerializer


'''
class TasksView(APIView):
    permission_classes = [IsAuthenticated]
    # serializer_class = TasksSerializer

    def patch(self, request, *args, **kwargs):
        tasks = get_object_or_404(Tasks, user_id=self.request.user.id)
        tasks.day_time = request.data.get
        if tasks.is_valid():
            tasks.save()
            return Response(status=status.HTTP_200_OK)
        print('NOT Valid')
        print(serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        

class TasksView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        tasks = get_object_or_404(Tasks, user_id=self.request.user.id)
        serializer = TasksSerializer(tasks, data=request.data, partial=True)
        if serializer.is_valid():
            print(serializer.validated_data['now_time'] >= 15 * (1 + self.request.user.level))
            print(not tasks.now_success)
            if serializer.validated_data['now_time'] >= 15 * (1 + self.request.user.level) and not tasks.now_success:
                print('111')
                serializer.now_success = True
                User.objects.update(energy=self.request.user.energy + self.request.user.level)
            if serializer.validated_data['day_time'] >= 20 * (5 + self.request.user.level) and not tasks.day_success:
                serializer.day_success = True
                User.objects.get(id=self.request.user.id).update(energy=self.request.user.energy + self.request.user.level)

            serializer.save()
            return Response(status=status.HTTP_200_OK)
        print('NOT valid')
        return Response(status=status.HTTP_408_REQUEST_TIMEOUT)
'''


class TasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(Tasks, user_id=self.request.user.id)
        instance.now_time += 5
        instance.day_time += 5
        instance.level_time += 5
        times_list = []
        if not instance.now_success and instance.now_time >= 15 * (1 + self.request.user.level):
            instance.now_success = True
            times_list.append('now')
        if not instance.day_success and instance.day_time >= 15 * (1 + self.request.user.level):
            instance.day_success = True
            times_list.append('day')
        if not instance.level_success and instance.level_time >= 15 * (1 + self.request.user.level):
            instance.level_success = True
            times_list.append('level')
        if times_list:
            user = User.objects.get(id=self.request.user.id)
            user.energy += len(times_list)
            user.save()
        instance.save()
        return Response(data=times_list, status=status.HTTP_200_OK)
