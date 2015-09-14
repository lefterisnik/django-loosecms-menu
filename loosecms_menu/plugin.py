# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from .models import *

from loosecms.plugin_pool import plugin_pool
from loosecms.plugin_modeladmin import PluginModelAdmin


class MenuInline(admin.StackedInline):
    model = Menu
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Menu.objects.filter(parent=None)
        return super(MenuInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class MenuManagerPlugin(PluginModelAdmin):
    model = MenuManager
    name = _('Menu')
    template = "plugin/menu.html"
    plugin = True
    inlines = [
        MenuInline,
    ]
    fieldsets = (
        (None, {
            'fields': ('type', 'placeholder', 'title', 'style', 'inverse', 'published')
        }),
        ('Brand options',{
            'classes': ('collapse',),
            'fields': ('brand_title', ('brand_image', 'brand_image_height'))
        }),
        ('Search options',{
            'classes': ('collapse',),
            'fields': ('search', 'search_page')
        })
    )

    def update_context(self, context, manager):
        menus = Menu.objects.select_related('page').filter(manager=manager, published=True)\
                                                   .order_by('order')\
                                                   .prefetch_related('menu_set')
        context['menus'] = menus
        context['menumanager'] = manager
        return context

plugin_pool.register_plugin(MenuManagerPlugin)