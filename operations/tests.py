from django.test import TestCase
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.test import APIClient
from .utils import calculate
from .models import Operation

# Tests created for different application levels

class OperationsTestCase(TestCase):
    # Main Operations Test Case Class
    def setUp(self):
        # Preparing API client, first operation register and login
        self.c = APIClient()
        values = [8.0, 8.0]
        operation_type = 'sum'
        self.u = User.objects.create_user("test", password='secret')
        Operation.objects.create(
            username=self.u,
            values=values,
            operation_type=operation_type,
            result=calculate(operation_type, values)
        )
        self.c.login(username='test', password='secret')

    def test_database_integrity(self):
        # Checking first registries on database
        user = User.objects.filter(username="test")
        self.assertEqual(user.exists(), True)
        self.assertEqual(Operation.objects.filter(username=user[0], id=1).exists(), True)
    
    def test_simple_calculations(self):
        # Checking simple calculations with just the function
        self.assertEqual(calculate("sum", [27.5, 10.0]), 37.5)
        self.assertEqual(calculate("sub", [98.5, 18.5]), 80.0)
        self.assertEqual(calculate("mul", [20.0, 10.0]), 200.0)
        self.assertEqual(calculate("div", [40.0, 10.0]), 4.0)
    
    def test_complex_calculations(self):
        # Checking complex calculations with just the function
        self.assertEqual(calculate("sum", [23.59, 68.47]), 92.06)
        self.assertEqual(calculate("sub", [75.00, 10.00, 2.00]), 63.00)
        self.assertEqual(calculate("mul", [28.37, 10.50, 3.00]), 893.655)
        self.assertEqual(calculate("div", [320.00, 64.00, 5.00]), 1.00)
    
    def test_calc_request(self):
        # Executing multiple requests for different operations, such as
        # sum, subtraction, multiplication, and division
        res1 = self.c.post('/operations/', {
            'values': [8.0, 8.0], 
            'operation_type': 'sum'
        }, format='json')
        self.assertEqual(res1.status_code, 201)
        self.assertEqual(res1.data, {
            'id': 2,
            'username': 'http://testserver/users/{}/' . format(self.u.pk),
            'operation_type': 'sum',
            'values': [8.0, 8.0],
            'result': 16.0
        })
        # Subtraction request
        res2 = self.c.post('/operations/', {
            'values': [24.0, 9.0],
            'operation_type': 'sub'
        }, format='json')
        self.assertEqual(res2.status_code, 201)
        self.assertEqual(res2.data, {
            'id': 3,
            'username': 'http://testserver/users/{}/' . format(self.u.pk),
            'operation_type': 'sub',
            'values': [24.0, 9.0],
            'result': 15.0
        })
        # Multiplication request
        res3 = self.c.post('/operations/', {
            'values': [2.0, 12.0],
            'operation_type': 'mul'
        }, format='json')
        self.assertEqual(res3.status_code, 201)
        self.assertEqual(res3.data, {
            'id': 4,
            'username': 'http://testserver/users/{}/' . format(self.u.pk),
            'operation_type': 'mul',
            'values': [2.0, 12.0],
            'result': 24.0
        })
        # Division request
        res4 = self.c.post('/operations/', {
            'values': [36.0, 2.0],
            'operation_type': 'div'
        }, format='json')
        self.assertEqual(res4.status_code, 201)
        self.assertEqual(res4.data, {
            'id': 5,
            'username': 'http://testserver/users/{}/' . format(self.u.pk),
            'operation_type': 'div',
            'values': [36.0, 2.0],
            'result': 18.0
        })
    def test_cache(self):
        # Checking write and read on cache
        cache.set('A', {
            'id': 1,
            'username': 'http://testserver/users/{}/' . format(self.u.pk),
            'operation': 'sum',
            'values': [24.0, 9.0],
            'result': 33.0
        })
        self.assertEqual(cache.get('A'), {
            'id': 1,
            'username': 'http://testserver/users/{}/' . format(self.u.pk),
            'operation': 'sum',
            'values': [24.0, 9.0],
            'result': 33.0
        })

    def tearDown(self):
        # Delete information from main cache and logotu
        cache.delete('A')
        self.c.logout()

class HealthTestCase(TestCase):
    # Simple test case for health check
    def setUp(self):
        self.c = APIClient()

    def test_health_endpoint(self):
        response = self.c.get('/health')
        self.assertEqual(response.status_code, 301)