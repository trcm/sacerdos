# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallfly', '0005_auto_20150401_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='address',
            field=models.CharField(unique=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='property',
            name='status',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
