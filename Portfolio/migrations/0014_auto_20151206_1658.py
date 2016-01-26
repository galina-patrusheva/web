# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0013_history'),
    ]

    operations = [
        migrations.RenameField(
            model_name='history',
            old_name='url',
            new_name='query',
        ),
    ]
