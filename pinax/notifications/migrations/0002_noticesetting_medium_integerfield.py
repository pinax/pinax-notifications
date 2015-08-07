# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial.py'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticesetting',
            name='medium',
            field=models.IntegerField(verbose_name='medium', choices=[(0, b'email')]),
        ),
    ]
