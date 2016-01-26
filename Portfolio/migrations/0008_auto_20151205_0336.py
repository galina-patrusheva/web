# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0007_visits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visits',
            name='user_agent',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
