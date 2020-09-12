import random
from rest_framework.views import APIView
from lots.serializers import NumberSerializer
from my_user.models import User
from number.models import Number
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from lot.permissions import ReadOnly
from lots.models import Lot
from number.service import choose_winners
from django.db import connection


class NumberListUpdateView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    @staticmethod
    def get(request, pk):
        lot_numbers_free = Number.objects.select_related('lot__creator').filter(lot_id=pk, owner_id=None)
        if lot_numbers_free:
            random_idx = random.randint(0, len(lot_numbers_free) - 1)
            lot_number = lot_numbers_free[random_idx]
            if lot_number.lot.energy > request.user.energy or lot_number.lot.creator == request.user:
                return Response(
                    data={'message': 'No have energy' if lot_number.lot.energy > request.user.energy else 'Your lot'},
                    status=status.HTTP_423_LOCKED
                )
            request.user.energy -= lot_number.lot.energy
            request.user.save(update_fields=['energy'])
            lot_number.owner = request.user
            lot_number.save()
            if len(lot_numbers_free) <= 1 and lot_number.lot.active:
                choose_winners(lot_number.lot)
            serializer = NumberSerializer(lot_number)
            print('7 %s' % len(connection.queries))
            return Response(
                data={'number': serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(
            data={'message': 'No have free numbers or ready number or you have'},
            status=status.HTTP_208_ALREADY_REPORTED
        )



