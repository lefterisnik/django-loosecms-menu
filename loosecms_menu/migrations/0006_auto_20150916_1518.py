# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_menu', '0005_auto_20150916_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menumanager',
            name='slug',
            field=models.SlugField(help_text='Give a slug for the menu manager.', unique=True, verbose_name='slug'),
        ),
    ]
