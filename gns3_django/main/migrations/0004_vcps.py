# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='VCPS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'VCPS Name')),
                ('vm_id', models.CharField(max_length=200, verbose_name=b'VM ID')),
                ('udp_port', models.CharField(max_length=10, verbose_name=b'UDP Port')),
                ('project', models.ForeignKey(to='main.Project')),
            ],
        ),
    ]
