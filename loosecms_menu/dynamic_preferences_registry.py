# -*- coding: utf-8 -*-
from dynamic_preferences.types import StringPreference
from dynamic_preferences import global_preferences_registry

# We start with a global preference
@global_preferences_registry.register
class SiteTitle(StringPreference):
    name = 'menu_brand_title'
    default = 'My site'