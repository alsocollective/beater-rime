# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetrack', '0006_auto_20150325_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='spreadsheet',
            name='url',
            field=models.CharField(max_length=2000, blank=True),
            preserve_default=True,
        ),
    ]
