from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, response
from rest_framework.permissions import AllowAny
from .models import Operation
from .serializers import UserSerializer, OperationSerializer

# Create your views here.

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer

class HealthViewSet(viewsets.ViewSet):
	permission_classes = (AllowAny, )
	def list(self, request, format=None):
		data = { "status": "up" }
		return response.Response(data)	