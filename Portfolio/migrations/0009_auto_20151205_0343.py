# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0008_auto_20151205_0336'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Visits',
            new_name='Visit',
        ),
    ]
