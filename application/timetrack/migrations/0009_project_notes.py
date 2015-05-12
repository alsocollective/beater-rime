# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetrack', '0008_auto_20150326_0029'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='notes',
            field=models.TextField(max_length=2000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
