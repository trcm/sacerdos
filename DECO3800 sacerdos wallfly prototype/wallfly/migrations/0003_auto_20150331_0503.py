# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallfly', '0002_auto_20150328_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='owner_name',
            field=models.CharField(default='Tom', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='property',
            name='property_image',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
    ]
