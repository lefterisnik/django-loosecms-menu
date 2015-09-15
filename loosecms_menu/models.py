# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models
from loosecms.models import Plugin, HtmlPage


class MenuManager(Plugin):
    default_type = 'MenuManagerPlugin'

    choices = (
        ('navbar-fixed-top', _('Fixed to top')),
        ('navbar-fixed-bottom', _('Fixed to bottom')),
    )

    title = models.CharField(_('title'), max_length=200,
                             help_text=_('Give a name for the menu manager.'))
    brand_title = models.CharField(_('brand title'), max_length=50, blank=True, default='My Site',
                                   help_text=_('Give the brand name of your site.'))
    brand_image = models.ImageField(_('brand image'), upload_to='images', blank=True,
                                    help_text=_('Upload the brand image'))
    brand_image_height = models.IntegerField(_('image height'), blank=True, default=20,
                                             help_text=_('Set the height of the image'))
    search = models.BooleanField(_('search'), default=False,
                                 help_text=_('Check this box if you like to appear a search box'))
    search_page = models.ForeignKey(HtmlPage, verbose_name=_('search_page'), blank=True, null=True,
                                    limit_choices_to={'is_template':False},
                                    help_text=_('Select the page to show the results. Page must have search plugin.'))
    ctime = models.DateTimeField(auto_now_add=True)

    utime = models.DateTimeField(auto_now=True)

    style = models.CharField(max_length=200, choices=choices, blank=True)

    inverse = models.BooleanField(_('inverse'), default=False)

    def __unicode__(self):
        return "%s (%s)" %(self.title, self.type)

    def clean(self):
        """
        Don't allow brand title and brand image to be set together
        Don't allow search box to be selected without search page setted up
        :return: cleaned_data and errors
        """
        if self.brand_title and self.brand_image:
            msg = _('Only one of the brand title or brand image can be setted up.')
            raise ValidationError({'brand_image': msg, 'brand_title': msg})

        if self.search and not self.search_page:
            msg_search = _('With checked the search box you should provide a page to show the results.')
            msg_search_page = _('You should provide a page to show the results.')
            raise ValidationError({'search': msg_search, 'search_page': msg_search_page })


class Menu(models.Model):
    title = models.CharField(_('title'), max_length=200,
                             help_text=_('Give the name of the menu entry.'))
    page = models.ForeignKey(HtmlPage, null=True, blank=True, verbose_name=_('page'),
                             limit_choices_to={'is_template':False},
                             help_text=_('Select the page to refer this menu entry.'))
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name=_('parent'),
                               help_text=_('If the menuitem is submenu select the parent menuitem.'))
    href = models.CharField(_('href'), max_length=50, blank=True,
                            help_text=_('Give the external url if this menu entry open external site.'))
    manager = models.ForeignKey(MenuManager, verbose_name=_('manager'),
                                help_text=_('Select the menu manager to attach this menu entry.'))
    order = models.IntegerField(_('order'), default=0)

    published = models.BooleanField(_('published'), default=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('menu')
        verbose_name_plural = _('menus')

    def clean(self):
        """
        Don't allow menu entries have the same order
        :return: cleaned_data and errors
        """
        if not self.page and not self.href:
            msg = _('You must provide at least one of the page or href field')
            raise  ValidationError({'page': msg, 'href': msg})

        if self.manager_id:
            menus = Menu.objects.filter(manager=self.manager)

            for menu in menus:
                if self.order == menu.order and self.parent == menu.parent and self.pk != menu.pk:
                    msg = _('In this place a menu entry is already exist. Please change the order.')
                    raise ValidationError({'order': msg})

    def decrease_order(self):
        old_order = self.order
        self.older = None
        self.save()

        menu = Menu.objects.get(manager=self.manager, parent=self.parent, order=old_order-1)
        if menu:
            menu.order += 1
            menu.save()

        self.order = old_order-1
        self.save()

    def increase_order(self):
        old_order = self.order
        self.older = None
        self.save()

        menu = Menu.objects.get(manager=self.manager, parent=self.parent, order=old_order+1)
        if menu:
            menu.order -= 1
            menu.save()

        self.order = old_order+1
        self.save()

