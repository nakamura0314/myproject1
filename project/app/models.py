import datetime
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class cost(models.Model):
    """その日の費用、naritoではスケジュールとして扱われている"""
    summary = models.CharField('概要', max_length=30)
    money = models.IntegerField(
        '金額', validators=[MinValueValidator(0), MaxValueValidator(100000000)])
    description = models.TextField('詳細な説明', blank=True)
    created_at = models.DateTimeField('日付', default=timezone.now)

    def __str__(self):
        return self.summary
