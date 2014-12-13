# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('describe', '0005_auto_20141213_0039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personmodel',
            name='was_choosen',
        ),
    ]
