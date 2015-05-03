# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallfly', '0008_auto_20150401_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='agent_id',
            field=models.ForeignKey(related_name='properties', to='wallfly.Agent', null=True),
            preserve_default=True,
        ),
    ]
