# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.text import slugify
from django.db import models, migrations

try:
    from unidecode import unidecode
except ImportError:
    unidecode = lambda slug: slug


def generate_slug_menumanager(apps, schema_editor):
    MenuManager = apps.get_model('loosecms_menu', 'MenuManager')
    for menumanager in MenuManager.objects.all():
        menumanager.slug = slugify(unidecode(menumanager.title))
        menumanager.save()


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_menu', '0004_auto_20150916_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='menumanager',
            name='slug',
            field=models.SlugField(help_text='Give a slug for the menu manager.', verbose_name='slug'),
        ),
        migrations.RunPython(generate_slug_menumanager),
    ]