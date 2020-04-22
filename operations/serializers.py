from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Operation
from functools import reduce
from operator import add, sub, mul, truediv


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class OperationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Operation
        fields = ['username', 'values', 'operation_type', 'result']
        read_only_fields = ['username', 'result']
    def create(self, validated_data):
        optype = validated_data['operation_type']
        operators = { 'SM': add, 'MU': sub, 'SB': mul, 'DV': truediv }
        values = [float(x) for x in validated_data['values'].split(',')]
        result = reduce(operators[optype], values)
        return Operation(
            username=self.context['request'].user,
            operation_type=validated_data['operation_type'],
            values=validated_data['values'],
            result=result
        )