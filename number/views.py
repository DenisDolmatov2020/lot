import datetime
import random
import pytz
from rest_framework.views import APIView
from lots.serializers import NumberSerializer
from my_user.models import User
from number.models import Number
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from lot.permissions import ReadOnly
from lots.models import Lot
from number.service import start_lot


class NumberListUpdateView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get_numbers(self, pk):
        lot_numbers = Number.objects.filter(lot_id=pk)
        step_energy = 0

        if self.request.user.id and lot_numbers:
            steps_count = lot_numbers.filter(owner_id=self.request.user.id).count()
            step_energy = lot_numbers[0].lot.energy * (2 ** steps_count)
        return lot_numbers, step_energy

    def patch(self, request, pk):
        lot_number = get_object_or_404(Number, pk=pk)
        if lot_number.owner:
            return Response(
                data={'message': 'Its number have owner'},
                status=status.HTTP_208_ALREADY_REPORTED
            )
        lot_numbers, step_energy = self.get_numbers(lot_number.lot.id)
        if lot_number.lot.creator == request.user:
            return Response(
                data={'message': 'Its self number'},
                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
            )
        user = get_object_or_404(User, id=request.user.id)
        if step_energy <= user.energy and request.user.id:
            lot_number.owner = request.user
            lot_number.save(update_fields=['owner'])
            if lot_number.owner:
                user.energy -= step_energy
                user.save(update_fields=['energy'])
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
        lot_numbers_free = Number.objects.filter(lot_id=pk).filter(owner_id=None)
        lot_numbers_free_count = lot_numbers_free.count()
        if lot_numbers_free_count:
            if Number.objects.filter(lot_id=pk).filter(owner_id=request.user.id).count() == 0:
                random_idx = random.randint(0, lot_numbers_free_count - 1)
                lot_number = lot_numbers_free[random_idx]
                user = get_object_or_404(User, id=request.user.id)
                if lot_number.lot.energy <= user.energy:
                    if lot_number.lot.creator == request.user:
                        return Response(
                            data={'message': 'Its self number'},
                            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
                        )
                    lot_number.owner = request.user
                    lot_number.save(update_fields=['owner'])
                    if lot_number.owner:
                        user.energy -= lot_number.lot.energy
                        user.save(update_fields=['energy'])
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
                Number.objects.filter(lot=lot, num__in=data_).update(won=True)
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


