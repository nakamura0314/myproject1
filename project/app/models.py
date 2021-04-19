import datetime
from django.utils import timezone
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Cost(models.Model):
    """その日の費用、naritoではスケジュールとして扱われている"""
    summary = models.CharField('カテゴリ', max_length=30)
    money = models.IntegerField(
        '金額', validators=[MinValueValidator(0), MaxValueValidator(100000000)])
    description = models.TextField('詳細な説明', blank=True)
    date = models.DateField('日付')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.summary
