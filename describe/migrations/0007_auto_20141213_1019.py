# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('describe', '0006_remove_personmodel_was_choosen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personmodel',
            name='present_description',
            field=models.TextField(verbose_name='Opisz swoj wymarzony prezent'),
            preserve_default=True,
        ),
    ]
