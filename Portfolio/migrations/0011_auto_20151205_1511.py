# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0010_counter'),
    ]

    operations = [
        migrations.RenameField(
            model_name='counter',
            old_name='views',
            new_name='total_views',
        ),
        migrations.RenameField(
            model_name='counter',
            old_name='visits',
            new_name='total_visits',
        ),
        migrations.AddField(
            model_name='counter',
            name='day_point',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 5, 10, 11, 57, 552370, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='counter',
            name='today_views',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='counter',
            name='today_visits',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
