# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-30 09:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('d19app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CTRecordModel',
            fields=[
                ('recordId', models.AutoField(primary_key=True, serialize=False)),
                ('recordTag', models.CharField(max_length=128)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='d19app.CTRUser')),
            ],
        ),
        migrations.CreateModel(
            name='CTRecordPoint',
            fields=[
                ('pointId', models.AutoField(primary_key=True, serialize=False)),
                ('recordDate', models.DateTimeField()),
                ('key', models.CharField(max_length=128)),
                ('index', models.IntegerField(default=0)),
                ('recordId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='d19app.CTRecordModel')),
            ],
        ),
    ]