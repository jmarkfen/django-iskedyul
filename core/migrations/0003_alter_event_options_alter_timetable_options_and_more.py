# Generated by Django 4.1.6 on 2023-03-20 13:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_block_event_rename_set_timetable'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={},
        ),
        migrations.AlterModelOptions(
            name='timetable',
            options={},
        ),
        migrations.AddField(
            model_name='timetable',
            name='interval',
            field=models.PositiveIntegerField(default=30, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(59)], verbose_name='interval'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='notes',
            field=models.CharField(default=None, max_length=240, verbose_name='notes'),
        ),
    ]
