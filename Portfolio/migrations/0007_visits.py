# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0006_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=64)),
                ('user_agent', models.CharField(max_length=256)),
                ('user_resolution', models.CharField(max_length=64, null=True)),
                ('datetime', models.DateTimeField()),
            ],
        ),
    ]
