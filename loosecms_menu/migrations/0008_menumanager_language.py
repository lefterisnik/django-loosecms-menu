# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_menu', '0007_auto_20150930_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='menumanager',
            name='language',
            field=models.BooleanField(default=False, help_text='Check this box if you like to appear a select box with available languages.', verbose_name='language'),
        ),
    ]
