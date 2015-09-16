# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_menu', '0003_auto_20150916_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='menumanager',
            name='slug',
            field=models.SlugField(default='asdasdadasd', help_text='Give a slug for the menu manager', unique=True, verbose_name='slug'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menumanager',
            name='title',
            field=models.CharField(help_text='Give a name for the menu manager.', unique=True, max_length=100, verbose_name='title'),
        ),
    ]
