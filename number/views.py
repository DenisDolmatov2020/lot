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
from django.db import connection


class NumberListUpdateView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get_numbers(self, pk):
        lot_numbers = Number.objects.filter(lot_id=pk)
        step_energy = 0

        if self.request.user.id and lot_numbers:
            steps_count = lot_numbers.filter(owner_id=self.request.user.id).count()
            step_energy = lot_numbers[0].lot.energy * (2 ** steps_count)
        return lot_numbers, step_energy

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
        print('CONNECTION')
        print(connection.queries)
        print(len(connection.queries))
        if not lot.start:
            lot.free = False
            # winners choose
            start_lot(lot)

    @staticmethod
    def check_free(pk, lot_numbers):
        lot_numbers_free = lot_numbers.filter(owner_id=None).select_related('lot')
        if lot_numbers_free.count() == 0:
            lot = Lot.objects.get(pk=pk)
            if not lot.start:
                lot_numbers_free.lot.active = False
                start_lot(lot)

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


