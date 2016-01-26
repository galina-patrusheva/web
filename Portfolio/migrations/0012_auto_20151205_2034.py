# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0011_auto_20151205_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='last_comment',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='prev_comment',
            field=models.ForeignKey(to='Portfolio.Comment', null=True),
        ),
    ]
