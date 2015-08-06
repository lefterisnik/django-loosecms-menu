# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from loosecms.models import Plugin, Page


class MenuManager(Plugin):
    choices = (
        ('navbar-fixed-top', _('Fixed to top')),
        ('navbar-fixed-bottom', _('Fixed to bottom')),
    )

    title = models.CharField(_('title'), max_length=200,
                             help_text=_('Give the name of the menu.'))
    ctime = models.DateTimeField(editable=False, auto_now_add=True)

    utime = models.DateTimeField(auto_now=True)

    style = models.CharField(max_length=200, choices=choices, blank=True)

    inverse = models.BooleanField(_('inverse'), default=False)

    published = models.BooleanField(_('published'), default=True)

    def __unicode__(self):
        return "%s (%s)" %(self.title, self.type)


class Menu(models.Model):
    title = models.CharField(_('title'), max_length=200,
                             help_text=_('Give the name of the menu entry.'))
    page = models.ForeignKey(Page, null=True, blank=True, verbose_name=_('page'),
                             help_text=_('Select the page to refer this menu entry.'))
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=_('parent'),
                               help_text=_('If the menuitem is submenu select the parent menuitem.'))
    href = models.CharField(_('href'), max_length=50, null=True, blank=True,
                            help_text=_('Give the external url if this menu entry open external site.'))
    manager = models.ForeignKey(MenuManager, verbose_name=_('manager'),
                                help_text=_('Select the menu manager to attach this menu entry.'))
    order = models.IntegerField(_('order'), default=0)

    published = models.BooleanField(_('published'), default=True)

    def __unicode__(self):
        return self.title