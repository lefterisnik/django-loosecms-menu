# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import MenuManager, Menu
from .plugin import MenuPlugin


class MenuAdmin(admin.ModelAdmin):
    list_filter = ('manager',)
    list_display = ('title', 'page', 'href', 'order', 'published')
    list_editable = ('published', 'order')
    search_fields = ['title',]

admin.site.register(MenuManager, MenuPlugin)
admin.site.register(Menu, MenuAdmin)
