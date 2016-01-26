# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0012_auto_20151205_2034'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('datetime', models.DateTimeField()),
                ('ip', models.CharField(max_length=32)),
                ('user_agent', models.CharField(max_length=256)),
                ('url', models.CharField(max_length=256)),
                ('user', models.ForeignKey(to='Portfolio.GalleryUser')),
            ],
        ),
    ]
