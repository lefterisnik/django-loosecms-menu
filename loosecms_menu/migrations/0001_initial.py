# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Give the name of the menu entry.', max_length=200, verbose_name='title')),
                ('href', models.CharField(help_text='Give the external url if this menu entry open external site.', max_length=50, null=True, verbose_name='href', blank=True)),
                ('order', models.IntegerField(default=0, verbose_name='order')),
                ('published', models.BooleanField(default=True, verbose_name='published')),
            ],
        ),
        migrations.CreateModel(
            name='MenuManager',
            fields=[
                ('plugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loosecms.Plugin')),
                ('title', models.CharField(help_text='Give a name for the menu manager.', max_length=200, verbose_name='title')),
                ('brand_title', models.CharField(default=b'My Site', help_text='Give the brand name of your site.', max_length=50, verbose_name='brand title', blank=True)),
                ('brand_image', models.ImageField(help_text='Upload the brand image', upload_to=b'images', verbose_name='brand image', blank=True)),
                ('brand_image_height', models.IntegerField(default=20, help_text='Set the height of the image', verbose_name='image height', blank=True)),
                ('search', models.BooleanField(default=False, help_text='Check this box if you like to appear a search box', verbose_name='search')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('utime', models.DateTimeField(auto_now=True)),
                ('style', models.CharField(blank=True, max_length=200, choices=[(b'navbar-fixed-top', 'Fixed to top'), (b'navbar-fixed-bottom', 'Fixed to bottom')])),
                ('inverse', models.BooleanField(default=False, verbose_name='inverse')),
                ('search_page', models.ForeignKey(blank=True, to='loosecms.HtmlPage', help_text='Select the page to show the results. Page must have search plugin.', null=True, verbose_name='search_page')),
            ],
            bases=('loosecms.plugin',),
        ),
        migrations.AddField(
            model_name='menu',
            name='manager',
            field=models.ForeignKey(verbose_name='manager', to='loosecms_menu.MenuManager', help_text='Select the menu manager to attach this menu entry.'),
        ),
        migrations.AddField(
            model_name='menu',
            name='page',
            field=models.ForeignKey(blank=True, to='loosecms.HtmlPage', help_text='Select the page to refer this menu entry.', null=True, verbose_name='page'),
        ),
        migrations.AddField(
            model_name='menu',
            name='parent',
            field=models.ForeignKey(blank=True, to='loosecms_menu.Menu', help_text='If the menuitem is submenu select the parent menuitem.', null=True, verbose_name='parent'),
        ),
    ]
