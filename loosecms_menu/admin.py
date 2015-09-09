# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Menu


class MenuAdmin(admin.ModelAdmin):
    list_filter = ('manager',)
    list_display = ('title', 'page', 'href', 'order', 'published')
    list_editable = ('published', 'order')
    search_fields = ['title',]

admin.site.register(Menu, MenuAdmin)
