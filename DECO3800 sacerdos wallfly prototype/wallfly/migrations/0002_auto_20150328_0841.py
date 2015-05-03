# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallfly', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financial',
            name='property_id',
            field=models.ForeignKey(to='wallfly.Property', null=True),
            preserve_default=True,
        ),
    ]
