# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0003_galleryuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryuser',
            name='confirm_token',
            field=models.CharField(default=0, max_length=128),
            preserve_default=False,
        ),
    ]
