# Generated by Django 4.1.6 on 2023-02-09 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Timeblock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'), ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday'), ('Sun', 'Sunday')], max_length=50)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('content', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'timeblock',
                'verbose_name_plural': 'timeblocks',
            },
        ),
        migrations.CreateModel(
            name='Timeset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('timeblocks', models.ManyToManyField(to='core.timeblock')),
            ],
            options={
                'verbose_name': 'timeset',
                'verbose_name_plural': 'timesets',
            },
        ),
    ]
