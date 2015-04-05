# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wallfly', '0006_auto_20150401_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='property_image',
            field=sorl.thumbnail.fields.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
    ]
