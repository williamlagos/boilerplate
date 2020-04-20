from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Operation

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class OperationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Operation
        fields = ['username', 'values', 'operation_type', 'result']
