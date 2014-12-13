# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('describe', '0004_randomizationmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='randomizationmodel',
            name='giving',
            field=models.IntegerField(unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='randomizationmodel',
            name='user_id',
            field=models.IntegerField(unique=True),
            preserve_default=True,
        ),
    ]
