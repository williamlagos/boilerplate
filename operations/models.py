from django.db import models
from django.contrib.auth.models import User
from django.core.validators import int_list_validator
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Operation(models.Model):
    class OperationType(models.TextChoices):
        SUM = 'SM', _('Sum')
        MUL = 'MU', _('Multiplication')
        SUB = 'SB', _('Subtraction')
        DIV = 'DV', _('Division')
    
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    values = models.TextField(validators=[int_list_validator])
    operation_type = models.CharField(
        max_length=2,
        choices=OperationType.choices,
        default=OperationType.SUM
    )
    result = models.FloatField()
