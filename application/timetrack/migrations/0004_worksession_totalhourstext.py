# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetrack', '0003_auto_20150316_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksession',
            name='totalhourstext',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
