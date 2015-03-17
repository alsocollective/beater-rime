# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetrack', '0004_worksession_totalhourstext'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksession',
            name='workType',
            field=models.CharField(default=b'design', max_length=9, choices=[(b'design', b'design'), (b'development', b'development'), (b'email', b'email'), (b'spagetti', b'spagetti'), (b'admin', b'admin')]),
            preserve_default=True,
        ),
    ]
