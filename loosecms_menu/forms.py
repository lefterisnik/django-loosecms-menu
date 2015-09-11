# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Menu


#TODO: Move to model class
class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = '__all__'

    def clean(self):
        """
        Don't allow menu entries have the same order
        :return: cleaned_data and errors
        """
        cleaned_data = super(MenuForm, self).clean()
        delete = False
        title = cleaned_data.get('title')
        manager = cleaned_data.get('manager')
        order = cleaned_data.get('order')

        menus = Menu.objects.filter(manager=manager)

        for menu in menus:
            if order == menu.order and title != menu.title:
                msg = _('In this place a menu entry is already exist. Please change the order.')
                self._errors['order'] = self.error_class([msg])
                delete = True
        if delete:
            del cleaned_data['order']

        return cleaned_data