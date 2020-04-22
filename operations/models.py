from django.db import models
from django.contrib.auth.models import User
from django.core.validators import int_list_validator
from django.utils.translation import gettext_lazy as _

# Calculator operations models for django database persistence layer

class Operation(models.Model):
    # Operation model, for storing multiple operands (in a list), 
    # operation type (sum, multiplication, subtraction or division),
    # result and user related to this calculation.
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
