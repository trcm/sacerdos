# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallfly', '0003_auto_20150331_0503'),
    ]

    operations = [
        migrations.AddField(
            model_name='wfuser',
            name='agent_id',
            field=models.ForeignKey(to='wallfly.Agent', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wfuser',
            name='owner_id',
            field=models.ForeignKey(to='wallfly.Owner', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wfuser',
            name='tentant_id',
            field=models.ForeignKey(to='wallfly.Tenant', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='wfuser',
            name='user_level',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
