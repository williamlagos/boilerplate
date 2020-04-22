from django.contrib.auth.models import User, Group
from django.core.cache import cache
from rest_framework import serializers, fields
from .models import Operation
from .utils import calculate

# Serializers that defines the API representation and the linking 
# between database (models), cache (dictionaries) and views.

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
        # Modified create operation to transform values list into string
        oper = Operation(
            username=self.context['request'].user,
            operation_type=validated_data['operation_type'],
            values=','.join(str(i) for i in validated_data['values']),
            result=calculate(validated_data['operation_type'], validated_data['values'])
        )
        oper.save()
        # Code for operation log storing on Redis cache
        cache.set(str(oper.id), {
            'id': oper.id,
            'username': self.context['request'].user.username,
            'operation': validated_data['operation_type'],
            'values': validated_data['values'],
            'result': oper.result
        })
        # Getting sure that the key doesn't have timeout
        cache.persist(str(oper.id))
        return oper
    
    def to_representation(self, instance: Operation):
        # Modified to_representation to transform string value into value list
        instance.values = [float(i) for i in instance.values.split(',')]
        return super(OperationSerializer, self).to_representation(instance)