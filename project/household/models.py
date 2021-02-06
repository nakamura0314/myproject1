import datetime
from django.db import models
from django.utils import timezone


class calendar(models.Model):
    """カレンダー"""
    money = models.InteherField(
        '金額',
        validators=[validators.MinValueValidator(0),
                    validators.MaxValueValidator(10000000)]
    )
    description = models.TextField('概要', blank=True)
    date = models.DateField('日付')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __int__(self):
        return self.money
