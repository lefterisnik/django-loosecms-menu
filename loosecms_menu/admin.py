# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import MenuManager, Menu
from .plugin import MenuPlugin

admin.site.register(MenuManager, MenuPlugin)
admin.site.register(Menu)
