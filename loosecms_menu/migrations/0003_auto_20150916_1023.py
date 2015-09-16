# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_menu', '0002_auto_20150914_2201'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'verbose_name': 'menu', 'verbose_name_plural': 'menus'},
        ),
        migrations.AddField(
            model_name='menu',
            name='is_alone',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='menu',
            name='is_first',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='menu',
            name='is_last',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
