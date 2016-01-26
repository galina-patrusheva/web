# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0014_auto_20151206_1658'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('photo', models.ForeignKey(to='Portfolio.Photo')),
                ('user', models.ForeignKey(to='Portfolio.GalleryUser')),
            ],
        ),
        migrations.AlterField(
            model_name='comment',
            name='prev_comment',
            field=models.ForeignKey(to='Portfolio.Comment', null=True, blank=True),
        ),
    ]
