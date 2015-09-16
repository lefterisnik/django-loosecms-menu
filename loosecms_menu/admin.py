# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

from .models import Menu


class MenuAdmin(admin.ModelAdmin):
    list_filter = ('manager', 'parent')
    list_display = ('title', 'manager', 'parent', 'page', 'href', 'get_move', 'published')
    list_editable = ('published',)
    search_fields = ('title',)
    list_select_related = ('parent', 'page', 'manager')
    ordering = ('parent', 'order')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Menu.objects.filter(parent=None)
        return super(MenuAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_move(self, obj):
        """
        Return links for move up and move donw
        :param obj:
        :return: html
        """
        button = u'<a href="%s"><span class="glyphicon glyphicon-arrow-%s"></span></a>'
        html = ''

        if not obj.is_alone:
            if not obj.is_first:
                link = '%d/move_up/' % obj.pk
                html = button % (link, 'up')

            if not obj.is_last:
                link = '%d/move_down/' % obj.pk
                if html:
                    html += button % (link, 'down')
                else:
                    html = button % (link, 'down')
        return html

    get_move.allow_tags = True
    get_move.short_description = _('Move')

    def get_urls(self):
        urls = [
            url(r'^(?P<pk>\d+)/move_up/$', self.admin_site.admin_view(self.move_up)),
            url(r'^(?P<pk>\d+)/move_down/$', self.admin_site.admin_view(self.move_down)),
        ]
        return urls + super(MenuAdmin, self).get_urls()

    def move_up(self, request, pk):
        """
        Increase order of menu
        :param request:
        :param pk:
        :return: changelist
        """
        if self.has_change_permission(request):
            item = get_object_or_404(Menu, pk=pk)
            item.decrease_order()
        else:
            raise PermissionDenied
        opts = self.model._meta
        return redirect('admin:%s_%s_changelist' % (opts.app_label, opts.model_name))

    def move_down(self, request, pk):
        """
        Decrease order of menu
        :param request:
        :param pk:
        :return: changelist
        """
        if self.has_change_permission(request):
            item = get_object_or_404(Menu, pk=pk)
            item.increase_order()
        else:
            raise PermissionDenied
        opts = self.model._meta
        return redirect('admin:%s_%s_changelist' % (opts.app_label, opts.model_name))

admin.site.register(Menu, MenuAdmin)
