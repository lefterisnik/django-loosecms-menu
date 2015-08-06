# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.template import loader

from .models import MenuManager, Menu
from .forms import MenuManagerForm, MenuForm

from loosecms.plugin_pool import plugin_pool
from loosecms.plugin_modeladmin import PluginModelAdmin


class MenuInline(admin.StackedInline):
    model = Menu
    form = MenuForm
    extra = 1


class MenuPlugin(PluginModelAdmin):
    model = MenuManager
    name = _('Menu')
    form = MenuManagerForm
    template = "plugin/menu.html"
    plugin = True
    inlines = [
        MenuInline,
    ]
    extra_initial_help = None

    def render(self, context, manager):
        menus = Menu.objects.select_related('page').filter(manager=manager).order_by('order').prefetch_related('menu_set')

        t = loader.get_template(self.template)
        context['menus'] = menus
        context['menumanager'] = manager
        return t.render(context)

    def get_changeform_initial_data(self, request):
        initial = {}
        if self.extra_initial_help:
            initial['type'] = self.extra_initial_help['type']
            initial['placeholder'] = self.extra_initial_help['placeholder']
            initial['manager'] = self.extra_initial_help['page']

            return initial
        else:
            return {'type': 'MenuPlugin'}

plugin_pool.register_plugin(MenuPlugin)