from django.contrib.auth.models import User
from django.db import connection
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser
from rest_framework.response import Response
from number.models import Number
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
    parser_classes = (MultiPartParser,)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        user_numbers = Number.objects.only('lot_id', 'num').filter(owner=request.user)
        numbers_dict = {number.lot_id: number.num for number in user_numbers}
        return Response(
            status=status.HTTP_200_OK,
            data={'user': serializer.data, 'numbers': numbers_dict}
        )

    def update(self, request, *args, **kwargs):
        serializer = UserSerializer(
            instance=request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

