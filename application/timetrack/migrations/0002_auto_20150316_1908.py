# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetrack', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksession',
            name='endTimeFloat',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='worksession',
            name='startTimeFloat',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='worksession',
            name='pauseEnd',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='worksession',
            name='pauseStart',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='worksession',
            name='startTime',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
