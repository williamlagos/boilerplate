from django.contrib.auth.models import User, Group
from django.core.cache import cache
from rest_framework import serializers, fields
from .models import Operation
from .utils import calculate

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class OperationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Operation
        fields = ['id', 'username', 'values', 'operation_type', 'result']
        read_only_fields = ['id', 'username', 'result']
    
    values = serializers.ListField(child=serializers.FloatField())

    def create(self, validated_data):
        oper = Operation(
            username=self.context['request'].user,
            operation_type=validated_data['operation_type'],
            values=','.join(str(i) for i in validated_data['values']),
            result=calculate(validated_data['operation_type'], validated_data['values'])
        )
        oper.save()
        cache.set(str(oper.id), {
            'id': str(oper.id),
            'username': self.context['request'].user.username,
            'operation': validated_data['operation_type'],
            'values': validated_data['values'],
            'result': oper.result
        })
        cache.persist(str(oper.id))
        return oper
    
    def to_representation(self, instance: Operation):
        instance.values = [float(i) for i in instance.values.split(',')]
        return super(OperationSerializer, self).to_representation(instance)