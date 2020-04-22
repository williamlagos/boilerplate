from django.db import models
from django.contrib.auth.models import User
from django.core.validators import int_list_validator
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Operation(models.Model):
    class OperationType(models.TextChoices):
        SUM = 'sum', _('Sum')
        MUL = 'mul', _('Multiplication')
        SUB = 'sub', _('Subtraction')
        DIV = 'div', _('Division')
    
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    values = models.TextField(validators=[int_list_validator])
    operation_type = models.CharField(
        max_length=3,
        choices=OperationType.choices,
        default=OperationType.SUM
    )
    result = models.FloatField()
