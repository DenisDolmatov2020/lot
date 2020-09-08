from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser
from rest_framework.response import Response

from lots.models import LotNumber
from my_user.serializers import UserSerializer
from rest_framework.generics import get_object_or_404, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model


User = get_user_model()


class UserCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    parser_class = (FileUploadParser,)

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        user_numbers = LotNumber.objects.filter(owner=request.user)
        d = {}
        for i in user_numbers:
            d[i.lot.id] = i.num
        return Response(status=status.HTTP_200_OK, data={'user': serializer.data, 'numbers': d})

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if request.data.get('name'):
            user.name = request.data.get('name')
        if request.data.get('image') and request.data.get('image') is not None:
            user.image = request.data.get('image')
        user.notification = request.data.get('notification') == 'true'
        user.sound = request.data.get('sound') == 'true'
        user.save()
        serializer = self.get_serializer(user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)