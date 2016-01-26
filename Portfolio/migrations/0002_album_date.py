# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 11, 17, 5, 47, 26, 571346, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
