# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetrack', '0002_auto_20150316_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksession',
            name='notes',
            field=models.TextField(max_length=1000, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='worksession',
            name='totalhours',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
