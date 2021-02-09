import datetime
from django.db import models
from django.utils import timezone


class cost(models.Model):
    """その日の費用、今はスケジュールとして扱う"""
