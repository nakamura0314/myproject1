# Generated by Django 3.2 on 2021-04-19 13:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cost',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日'),
        ),
    ]
