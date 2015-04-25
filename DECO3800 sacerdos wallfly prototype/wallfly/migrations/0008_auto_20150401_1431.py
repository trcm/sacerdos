# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('wallfly', '0007_auto_20150401_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='property_image',
            field=django_resized.forms.ResizedImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
    ]
