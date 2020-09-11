from rest_framework import serializers
from number.models import Number
from my_user.serializers import UserSerializer


class NumberSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Number
        fields = ['id', 'lot', 'owner', 'num']
