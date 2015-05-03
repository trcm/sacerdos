# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallfly', '0004_auto_20150401_0809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wfuser',
            name='tentant_id',
        ),
        migrations.AddField(
            model_name='wfuser',
            name='tenant_id',
            field=models.ForeignKey(blank=True, to='wallfly.Tenant', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wfuser',
            name='agent_id',
            field=models.ForeignKey(blank=True, to='wallfly.Agent', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wfuser',
            name='owner_id',
            field=models.ForeignKey(blank=True, to='wallfly.Owner', null=True),
            preserve_default=True,
        ),
    ]
