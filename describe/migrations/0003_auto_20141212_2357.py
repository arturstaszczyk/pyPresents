# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('describe', '0002_auto_20141212_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='personmodel',
            name='was_choosen',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personmodel',
            name='present_description',
            field=models.TextField(verbose_name=b'Opisz swoj wymarzony prezent'),
            preserve_default=True,
        ),
    ]
