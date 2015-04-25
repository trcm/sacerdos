# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('agent_id', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('contact_num', models.CharField(max_length=12)),
                ('real_estate', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=75)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Financial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('property_id', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('rent_amount', models.IntegerField()),
                ('day_of_payment', models.CharField(max_length=10, null=True, choices=[(b'Monday', b'Mon'), (b'Tuesday', b'Tues'), (b'Wednesday', b'Wed'), (b'Thursday', b'Thurs'), (b'Friday', b'Fri')])),
                ('payment_type', models.CharField(max_length=50, null=True)),
                ('payment_due', models.IntegerField(null=True)),
                ('payment_status', models.IntegerField(default=1, null=True)),
                ('bond', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('issue_id', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('severity', models.IntegerField(default=1)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('image', models.ImageField(null=True, upload_to=b'')),
                ('resolved', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('owner_id', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('contact_number', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=75)),
                ('num_properties', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('property_id', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('address', models.CharField(max_length=200)),
                ('status', models.IntegerField(unique=True)),
                ('num_tenants', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=200)),
                ('property_image', models.ImageField(upload_to=b'')),
                ('agent_id', models.ForeignKey(to='wallfly.Agent', null=True)),
                ('owner_id', models.ForeignKey(to='wallfly.Owner', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tenant_id', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('contact_number', models.CharField(max_length=20, null=True)),
                ('email', models.EmailField(max_length=75)),
                ('previous_address', models.CharField(max_length=200, null=True)),
                ('extra_information', models.CharField(max_length=200, null=True)),
                ('property_id', models.ForeignKey(to='wallfly.Property', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WFUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='issue',
            name='property_id',
            field=models.ForeignKey(to='wallfly.Property', null=True),
            preserve_default=True,
        ),
    ]
