from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dataset


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']


class DatasetSerializer(serializers.ModelSerializer):
    """
    Serializer for Dataset model.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Dataset
        fields = [
            'id',
            'name',
            'upload_timestamp',
            'total_equipment',
            'average_flowrate',
            'average_pressure',
            'average_temperature',
            'type_distribution',
            'username'
        ]
        read_only_fields = ['id', 'upload_timestamp', 'username']


class SummarySerializer(serializers.Serializer):
    """
    Serializer for summary response.
    """
    total_equipment = serializers.IntegerField()
    average_values = serializers.DictField()
    type_distribution = serializers.DictField()
    upload_date = serializers.DateTimeField(required=False)
    dataset_name = serializers.CharField(required=False)