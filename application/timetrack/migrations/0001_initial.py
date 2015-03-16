# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('slug', models.SlugField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('completed', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startTime', models.DateTimeField(auto_now=True)),
                ('endTime', models.DateTimeField(null=True, blank=True)),
                ('completed', models.BooleanField(default=False)),
                ('minusTime', models.FloatField(default=0)),
                ('pauseStart', models.DateTimeField(null=True, blank=True)),
                ('pauseEnd', models.DateTimeField(null=True, blank=True)),
                ('person', models.ForeignKey(to='timetrack.Person')),
                ('project', models.ForeignKey(to='timetrack.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='person',
            name='lastProject',
            field=models.ForeignKey(blank=True, to='timetrack.Project', null=True),
            preserve_default=True,
        ),
    ]
