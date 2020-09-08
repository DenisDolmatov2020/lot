from rest_framework import serializers
from company.models import Company


class CompanySerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Company
        fields = [
            'user_id',
            'name',
            'phrase',
            'count_games',
            'count_rating',
            'image',
            'color',
            'color_type',
            'color_text'
        ]
