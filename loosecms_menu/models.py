# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Max, Min
from django.db.models.signals import post_delete
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from loosecms.models import Plugin, HtmlPage

from .signals import menu_delete


class MenuManager(Plugin):
    default_type = 'MenuManagerPlugin'

    choices = (
        ('navbar-fixed-top', _('Fixed to top')),
        ('navbar-fixed-bottom', _('Fixed to bottom')),
    )

    title = models.CharField(_('title'), max_length=100, unique=True,
                             help_text=_('Give a name for the menu manager.'))
    slug = models.SlugField(_('slug'), unique=True,
                            help_text=_('Give a slug for the menu manager'))
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

    is_first = models.BooleanField(default=False, editable=False)

    is_last = models.BooleanField(default=False, editable=False)

    is_alone = models.BooleanField(default=False, editable=False)

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
            raise ValidationError({'page': msg, 'href': msg})

        if self.page and self.href:
            msg = _('You must provide either the page or the href field, not both.')
            raise ValidationError({'page': msg, 'href': msg})

        if self.manager_id:
            menus = Menu.objects.filter(manager=self.manager)

            for menu in menus:
                if self.order == menu.order and self.parent == menu.parent and self.pk != menu.pk:
                    msg = _('In this place a menu entry is already exist. Please change the order.')
                    raise ValidationError({'order': msg})

    def save(self, *args, **kwargs):
        """
        Update menus position
        :param commit:
        :return: None
        """
        # Fetch all menus with the same parent of the current, excluding this
        menus_with_same_parent = Menu.objects.filter(parent=self.parent, manager=self.manager)\
            .exclude(pk=self.pk)

        # If one menu exists then make it not alone and first or last depending the order
        if menus_with_same_parent.count() == 1:
            # In changing position the first save will not trigger any if because self.order and other menu they have
            # the same order. In the last save will trigger the appropriate if and it will change the other menu
            # to opposite values.
            if self.order > menus_with_same_parent[0].order:
                self.is_last = True
                self.is_first = False
                menus_with_same_parent.update(is_alone=False, is_last=False, is_first=True)
            elif self.order < menus_with_same_parent[0].order:
                self.is_first = True
                self.is_last = False
                menus_with_same_parent.update(is_alone=False, is_first=False, is_last=True)
        elif menus_with_same_parent.count() != 0:
            # More comlex!!! In changing position the first save will trigger the appropriate 'if' because of the equal.
            # For example: if move up is pressed on a middle menu item, then the first save action will be fired by
            # the menu that holding the max min order. In this case will be triggered the last if and the second save
            # action will trigger the last if, if menu keep holding a middle position, otherwise will be triggered the
            # appropriate if depending of the maximum or minimum order that it has.
            menu_order = menus_with_same_parent.aggregate(max_order=Max('order'), min_order=Min('order'))
            if self.order >= menu_order['max_order']:
                self.is_last = True
                menus_with_same_parent.filter(is_last=True).update(is_last=False)
            elif self.order <= menu_order['min_order']:
                self.is_first = True
                menus_with_same_parent.get(is_last=True).update(is_first=False)
            else:
                self.is_last = False
                self.is_first = False
        else:
            self.is_alone = True
            self.is_first = True
            self.is_last = True
        super(Menu, self).save(*args, **kwargs)

    def decrease_order(self):
        """
        Move the menu one step above and move below the menu that holding this order if exists
        :return: None
        """
        old_order = self.order

        menu = Menu.objects.filter(manager=self.manager, parent=self.parent, order__lt=old_order)
        if menu:
            menu_with_max_min_order = menu.aggregate(max_min_order=Max('order'))
            menu = menu.get(order=menu_with_max_min_order['max_min_order'])
            menu.order = old_order
            menu.save()

        self.order = menu_with_max_min_order['max_min_order']
        self.save()

    def increase_order(self):
        """
        Move the menu one step below and move above the menu that holding this order if exists
        :return:
        """
        old_order = self.order

        menu = Menu.objects.filter(manager=self.manager, parent=self.parent, order__gt=old_order)
        if menu:
            menu_with_min_max_order = menu.aggregate(min_max_order=Min('order'))
            menu = menu.get(order=menu_with_min_max_order['min_max_order'])
            menu.order = old_order
            menu.save()

        self.order = menu_with_min_max_order['min_max_order']
        self.save()

post_delete.connect(menu_delete, Menu)