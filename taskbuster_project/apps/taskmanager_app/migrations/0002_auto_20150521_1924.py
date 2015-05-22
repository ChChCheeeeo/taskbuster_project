# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, help_text='Enter the project name', verbose_name='name')),
                ('color', models.CharField(validators=[django.core.validators.RegexValidator('(^#[0-9a-fA-F]{3}$)|(^#[0-9a-fA-F]{6}$)')], max_length=7, help_text='Enter the hex color code, like #ccc or #cccccc', default='#fff', verbose_name='color')),
                ('user', models.ForeignKey(verbose_name='user', to='taskmanager_app.Profile', related_name='projects')),
            ],
            options={
                'ordering': ('user', 'name'),
                'verbose_name_plural': 'Projects',
                'verbose_name': 'Project',
            },
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('user', 'name')]),
        ),
    ]
