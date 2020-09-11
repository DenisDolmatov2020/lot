from rest_framework import serializers
from lots.models import Lot, Condition
from my_user.serializers import UserSerializer
from number.serializers import NumberSerializer


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = '__all__'
        read_only_fields = ('lot',)


class LotSerializer(serializers.ModelSerializer):
    # conditions = ConditionSerializer(many=True, required=False)
    creator = UserSerializer(read_only=True)
    conditions = ConditionSerializer(many=True, read_only=True)
    wins = NumberSerializer(many=True, read_only=True)

    class Meta:
        model = Lot
        fields = [
            'id',
            'creator',
            'title',
            'description',
            'image',
            'players',
            'winners',
            'energy',
            'free',
            'active',
            'start',
            'wins',
            'conditions'
        ]


class LotSaveSerializer(serializers.ModelSerializer):
    # creator = UserCompanySerializer(read_only=True)
    conditions = ConditionSerializer(many=True)
    # conditions = serializers.PrimaryKeyRelatedField(many=True, read_only=True, allow_null=True)

    class Meta:
        model = Lot
        fields = [
            'id',
            'creator',
            'title',
            'description',
            'image',
            'image_two',
            'image_three',
            'image_four',
            'players',
            'winners',
            'energy',
            'free',
            'active',
            'start',
            'conditions',
        ]

    def create(self, validated_data):
        conditions_data = validated_data.pop('conditions', [])
        lot = Lot.objects.create(**validated_data)
        if conditions_data:
            Condition.objects.bulk_create(
                Condition(lot=lot, **condition)
                for condition in conditions_data
            )
        return lot
