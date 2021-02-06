import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


class calendar(models.Model):
    """カレンダー"""
    money = models.IntegerField(
        verbose_name='金額',
        default=0,
        validators=[MinValueValidator(0),
                    MaxValueValidator(10000000)]
    )
    description = models.TextField('概要', blank=True)
    date = models.DateField('日付')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __int__(self):
        return self.money
