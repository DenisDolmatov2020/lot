import datetime
from collections import namedtuple
# Create your views here.
import random
import pytz
from rest_framework import viewsets, status
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from lots.models import Lot, LotNumber, Condition
from lots.serializers import LotSerializer, NumberSerializer, LotSaveSerializer, ConditionSerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser

from my_user.models import User
import requests
from .service import start_lot
from django.db.models import ManyToOneRel


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


'''class LotsViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    file_content_parser_classes = (JSONParser, FileUploadParser)
    permission_classes = [AllowAny | ReadOnly]
    # serializer_class = LotSaveSerializer
    # queryset = Lot.objects.all()

    def get_queryset(self):
        if self.action == 'list':
            return Lot.objects.filter(free=True).filter(active=True)
        return Lot.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return LotSaveSerializer
        return LotSerializer'''


class WinnersList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        winners = LotNumber.objects.filter(won=True)
        serializer_winners = NumberSerializer(winners, many=True)
        lots = Lot.objects.all()
        serializer_lots = LotSerializer(lots, many=True)
        return Response(data={
            'lots': serializer_lots.data,
            'winners': serializer_winners.data
        }, status=status.HTTP_200_OK)


class LotViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser, FileUploadParser)
    file_content_parser_classes = (JSONParser, FileUploadParser)
    permission_classes = [AllowAny | ReadOnly]
    serializer = LotSerializer

    @staticmethod
    def list(request, *args):
        lots = Lot.objects.all()
        # annotate(wins=LotNumber.objects.filter(won=True))
        for lot in lots:
            if lot.free:
                lot.conditions = Condition.objects.filter(lot_id=lot.id)
            else:
                wins = LotNumber.objects.filter(lot_id=lot.id, won=True)
                if len(wins):
                    lot.wins = wins
                '''else:
                    lot.wins = start_lot(lot)'''
            # print(connection.queries)

        # filter(free=True).filter(active=True)
        serializer = LotSerializer(lots, many=True)
        return Response(serializer.data)

    @staticmethod
    def retrieve(request, pk=None, *args):
        queryset = Lot.objects.all()
        lot = get_object_or_404(queryset, pk=pk)
        serializer = LotSerializer(lot)
        return Response(serializer.data)

    @staticmethod
    def create(request, *args):
        conditions = request.data.get('conditions')
        data_ = request.data.dict()
        data_['conditions'] = json.loads(conditions)
        serializer = LotSaveSerializer(data=data_)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    '''
        print(serializer)
        lot = serializer.save()
        conditions = [{"link": "https://twitter.com/account/access", "value": "i", "icon": "mdi-twitter", "color": "cyan","title":"Twitter","actions":["Подписка"]}, {"link":"https://twitter.com/account/access","value":"i","icon":"mdi-twitter","color":"cyan","title":"Twitter","actions":["Подписка"]}]
        serializer_conditions = ConditionSerializer(data=conditions, many=True)
        print(serializer_conditions.is_valid(raise_exception=True))
        if serializer_conditions.is_valid():
            print('1')
            print(serializer_conditions.data)
            serializer_conditions.save(lot_id=lot.id)
        print(serializer_conditions)
    '''


class NumberListUpdateView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get_numbers(self, pk):
        lot_numbers = LotNumber.objects.filter(lot_id=pk)
        step_energy = 0

        if self.request.user.id and lot_numbers:
            steps_count = lot_numbers.filter(owner_id=self.request.user.id).count()
            step_energy = lot_numbers[0].lot.energy * (2 ** steps_count)
        return lot_numbers, step_energy

    def patch(self, request, pk, format=None):
        print('Start PATCH !')
        lot_number = get_object_or_404(LotNumber, pk=pk)
        if lot_number.owner:
            return Response(data={'message': 'Its number have owner'}, status=status.HTTP_208_ALREADY_REPORTED)
        lot_numbers, step_energy = self.get_numbers(lot_number.lot.id)
        user = get_object_or_404(User, id=self.request.user.id)
        if step_energy <= user.energy and self.request.user.id:
            if lot_number.lot.creator == self.request.user:
                return Response(
                    data={'message': 'Its self number'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                )
            lot_number.owner = self.request.user
            lot_number.save()
            if lot_number.owner:
                user.energy -= step_energy
                user.save()
            self.check_free(lot_number.lot.id, lot_numbers)
            next_step_energy = step_energy * 2 - user.karma
            if next_step_energy < 1:
                next_step_energy = 1

            serializer = NumberSerializer(lot_number)
            return Response(data={'number': serializer.data,
                                  'step_energy': next_step_energy,
                                  'user_energy': user.energy},
                            status=status.HTTP_200_OK)
        else:
            return Response(
                data={'message': 'No have energy', 'energy_user': user.energy, 'energy_step': step_energy},
                status=status.HTTP_205_RESET_CONTENT
            )

    def post(self, request, pk):
        lot_numbers_free = LotNumber.objects.filter(lot_id=pk).filter(owner_id=None)
        lot_numbers_free_count = lot_numbers_free.count()
        if lot_numbers_free_count:
            if LotNumber.objects.filter(lot_id=pk).filter(owner_id=request.user.id).count() == 0:
                random_idx = random.randint(0, lot_numbers_free_count - 1)
                lot_number = lot_numbers_free[random_idx]
                user = get_object_or_404(User, id=request.user.id)
                if lot_number.lot.energy <= user.energy:
                    if lot_number.lot.creator == request.user:
                        return Response(
                            data={'message': 'Its self number'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                        )
                    lot_number.owner = request.user
                    lot_number.save()
                    if lot_number.owner:
                        user.energy -= lot_number.lot.energy
                        user.save()
                    if lot_numbers_free_count == 1:
                        self.start_lot(lot_number.lot.id)

                    serializer = NumberSerializer(lot_number)
                    return Response(
                        data={'number': serializer.data, 'user_energy': user.energy},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        data={'message': 'No have energy', 'energy_user': user.energy},
                        status=status.HTTP_205_RESET_CONTENT
                    )
            else:
                return Response(
                    data={'message': 'You have number this lot'},
                    status=status.HTTP_207_MULTI_STATUS
                )
        else:
            lot = Lot.objects.get(id=pk)
            lot.active = False
            lot.free = False
            lot.save()
            return Response(
                data={'message': 'No have free numbers or ready number'},
                status=status.HTTP_208_ALREADY_REPORTED
            )

    @staticmethod
    def start_lot(pk):
        lot = Lot.objects.get(pk=pk)
        if not lot.start:
            lot.free = False
            # winners choose
            start_lot(lot)

    @staticmethod
    def check_free(pk, lot_numbers):
        lot_numbers_free = lot_numbers.filter(owner_id=None).count()
        if lot_numbers_free == 0:
            lot = Lot.objects.get(pk=pk)
            if not lot.start:
                lot.free = False

                # winners choose
                url = 'https://api.random.org/json-rpc/2/invoke'
                json_ = {
                    "jsonrpc": "2.0",
                    "method": "generateIntegers",
                    "params": {
                        "apiKey": "fc702e8a-53f0-4dc1-83f2-63c07fb0e835",
                        "n": lot.winners,
                        "min": 1,
                        "max": lot.players,
                        "replacement": False
                    },
                    "id": 1
                }
                r = requests.post(url, json=json_)
                json_ = json.loads(r.text)
                lot.winners_complete = json_['result']['random']['completionTime']
                data_ = json_['result']['random']['data']

                LotNumber.objects.filter(lot=lot, num__in=data_).update(won=True)

                last = Lot.objects.latest('start')
                now_time = datetime.datetime.now(datetime.timezone.utc)
                if not last.start or last.start < now_time:
                    lot.start = now_time
                else:
                    lot.start = last.start
                lot.start += datetime.timedelta(hours=1)
                if lot.start.hour > 21 or lot.start.hour < 7:
                    if lot.start.hour > 21:
                        lot.start += datetime.timedelta(days=1)
                    lot.start = datetime.datetime(
                        lot.start.year,
                        lot.start.month,
                        lot.start.day,
                        7,
                        tzinfo=pytz.UTC
                    )
                lot.save()

    def get(self, request, pk):
        lot_numbers, step_energy = self.get_numbers(pk)
        self.check_free(pk, lot_numbers)
        if lot_numbers:
            serializer = NumberSerializer(lot_numbers, many=True)
            if request.user.id:
                step_energy -= request.user.karma
            if step_energy < 1:
                step_energy = 1
            return Response(data={'numbers': serializer.data, 'step_energy': step_energy},
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TimelinesList(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = LotSerializer
    queryset = Lot.objects.filter(free=False)


class WinnersList(APIView):
    permission_classes = [AllowAny]
    serializer_class = NumberSerializer

    def get(self, request):
        winners = LotNumber.objects.filter(won=True)
        serializer = NumberSerializer(winners, many=True)
        return Response(data={'winners': serializer.data}, status=status.HTTP_200_OK)
