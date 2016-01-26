# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0005_auto_20151202_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('text', models.CharField(max_length=256)),
                ('datetime', models.DateTimeField()),
                ('author', models.ForeignKey(to='Portfolio.GalleryUser')),
                ('photo', models.ForeignKey(to='Portfolio.Photo')),
            ],
        ),
    ]
