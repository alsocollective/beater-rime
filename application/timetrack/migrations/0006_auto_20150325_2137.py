# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetrack', '0005_worksession_worktype'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpreadSheet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1000)),
                ('slug', models.SlugField(blank=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='person',
            name='sheet',
            field=models.ForeignKey(blank=True, to='timetrack.SpreadSheet', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='sheet',
            field=models.ForeignKey(blank=True, to='timetrack.SpreadSheet', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='worksession',
            name='sheet',
            field=models.ForeignKey(blank=True, to='timetrack.SpreadSheet', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='worksession',
            name='workType',
            field=models.CharField(default=b'', max_length=12, choices=[(b'design', b'design'), (b'development', b'development'), (b'email', b'email'), (b'spagetti', b'spagetti'), (b'admin', b'admin')]),
            preserve_default=True,
        ),
    ]
