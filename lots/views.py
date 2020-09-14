from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from lot.permissions import ReadOnly
from lots.models import Lot, Condition
from lots.serializers import LotSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser
from number.models import Number


class LotViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser, FileUploadParser)
    file_content_parser_classes = (JSONParser, FileUploadParser)
    permission_classes = [AllowAny | ReadOnly]
    queryset = Lot.objects.all()
    serializer = LotSerializer

    def list(self, request, *args):
        serializer = self.serializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args):
        lot = get_object_or_404(self.queryset, pk=pk)
        if lot.active:
            lot.conditions = Condition.objects.filter(lot_id=lot.id)
        else:
            lot.wins = Number.objects.filter(lot_id=lot.id, won=True)
        serializer = self.serializer(lot)
        return Response(serializer.data)

    @staticmethod
    def create(request, *args):
        conditions = request.data.get('conditions')
        data_ = request.data.dict()
        data_['conditions'] = json.loads(conditions)
        data_['user_id'] = request.user.id
        serializer = LotSerializer(data=data_)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.data)
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TimelinesList(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = LotSerializer
    queryset = Lot.objects.filter(active=False)
