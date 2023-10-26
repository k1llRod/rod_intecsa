# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 Eagle IT now <http://www.eagle-erp.com/>
# See LICENSE file for full copyright and licensing details.
#
##############################################################################
{
    'name': 'Sale Product By Location',
    'version': '13.0.1',
    'category': 'Sales',
    'summary': 'Define a specific source location on each Sale Order Line',

    'author': 'Eagle IT now',
    'website': 'http://www.eagle-erp.com/',
    'license': 'Other proprietary',

    'description': """
Sale Product By Location
========================
Allows to define a specific source location on each Sale Order line and sell the
products from the different locations, that may not be children of the default
location of the same SO picking type.
    """,

    'depends': ['base', 'sale_management', 'sale_stock'],
    'data': [
            'views/sale_view.xml',
        ],
    'images': ['images/EagleITnow_screenshot.png'],

    'price': 15.0,
    'currency': 'EUR',

    'installable': True,
    'application': False,
    'auto_install': False
}
