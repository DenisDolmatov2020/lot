from rest_framework import serializers
from my_user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'image',
            'stars',
            'energy',
            'diamonds',
            'karma',
            'level',
            'sound',
            'notification',
        ]
