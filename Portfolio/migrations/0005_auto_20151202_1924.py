# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0004_galleryuser_confirm_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galleryuser',
            name='confirm_token',
            field=models.CharField(null=True, max_length=128),
        ),
    ]
