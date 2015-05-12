# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetrack', '0007_spreadsheet_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkTypes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('short', models.CharField(max_length=500)),
                ('slug', models.SlugField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='worksession',
            name='workType',
        ),
        migrations.AddField(
            model_name='worksession',
            name='workTypes',
            field=models.ForeignKey(blank=True, to='timetrack.WorkTypes', null=True),
            preserve_default=True,
        ),
    ]
