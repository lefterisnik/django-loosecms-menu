# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='href',
            field=models.CharField(default='', help_text='Give the external url if this menu entry open external site.', max_length=50, verbose_name='href', blank=True),
            preserve_default=False,
        ),
    ]
