from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import DatabaseError
from django.core.cache import cache
from logging import getLogger
from redis.exceptions import ConnectionError
from rest_framework import viewsets, response
from rest_framework.permissions import AllowAny
from .models import Operation
from .serializers import UserSerializer, OperationSerializer

# ViewSets defining the view behavior for models and endpoints.

class UserViewSet(viewsets.ModelViewSet):
    """ 
    User handling API endpoint 
    list: List registered users
    retrieve: Get one user based on ID
    update: Update specific user based on ID
    create: Create one user with specified information
    partial_update: Update partially an existent user
    destroy: Delete one specific user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OperationViewSet(viewsets.ModelViewSet):
    """ 
    Calculator operations handling API endpoint 
    list: List calculated operations
    retrieve: Get one specific operation by ID
    update: Update specific operation based on ID
    create: Make a new operation with multiple operands
    partial_update: Update partially an existent operation
    destroy: Delete one specific operation
    """
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer

class HealthViewSet(viewsets.ViewSet):
    """ 
    ViewSet created for check system health by trying to connect
    on database and cache, then catching exceptions when one goes down.
    """
    permission_classes = (AllowAny, )
    def list(self, request, format=None):
        log = getLogger()
        data = { 
            'database_status': 'up',
            'cache_status': 'up'
        }
        try:
            log.info("Trying to connect to database and cache...")
            User.objects.all()
            cache.set('X', 'Y')
        except DatabaseError:
            log.error("Database is down. Check the connection on settings.")
            data['database_status'] = 'down'
        except ConnectionError:
            log.error("Cache is down. Check the connection on settings.")
            data['cache_status'] = 'down'
        return response.Response(data)	