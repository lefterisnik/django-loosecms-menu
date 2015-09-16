# -*- coding: utf-8 -*-
from django.db.models import Min, Max


def menu_delete(sender, instance, using, **kwargs):
    """
    Update menus positions
    :param sender:
    :param instance:
    :param using:
    :param kwargs:
    :return: None
    """
    # Fetch all menus with the same parent of the current, excluding this
    menus_with_same_parent = sender.objects.filter(parent=instance.parent, manager=instance.manager)\
        .exclude(pk=instance.pk)

    if menus_with_same_parent.count() == 1:
        # If one menu remain for this parent then make it alone, first and last
        menus_with_same_parent.update(is_alone=True, is_first=True, is_last=True)
    else:
        menu_order = menus_with_same_parent.aggregate(max_order=Max('order'), min_order=Min('order'))
        if instance.is_last:
            # If is last then make last the menu with the maximum order
            menus_with_same_parent.filter(order=menu_order['max_order']).update(is_last=True)
        if instance.is_first:
            # If is first the make first the menu with the smallest order
            menus_with_same_parent.filter(order=menu_order['min_order']).update(is_first=True)