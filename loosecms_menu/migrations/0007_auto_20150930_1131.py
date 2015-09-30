# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_menu', '0006_auto_20150916_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='parent',
            field=models.ForeignKey(related_name='submenus', blank=True, to='loosecms_menu.Menu', help_text='If the menuitem is submenu select the parent menuitem.', null=True, verbose_name='parent'),
        ),
    ]
