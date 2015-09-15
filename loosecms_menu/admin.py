# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Menu


class MenuAdmin(admin.ModelAdmin):
    list_filter = ('manager',)
    list_display = ('title', 'manager', 'page', 'href', 'order', 'published')
    list_editable = ('published', 'order')
    search_fields = ['title',]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Menu.objects.filter(parent=None)
        return super(MenuAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Menu, MenuAdmin)
