# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Disable Quick Create Product and User Restriction For Creating Product',
    'version': '13.0.0.1.0',
    'license': 'OPL-1',
    'summary': 'Disable Quick Create Product and User Restriction For Creating Product',
    'sequence': 1,
    "author": "Alphasoft",
    'description': """
Account Voucher
====================
    """,
    'category' : 'Tools',
    'website': 'https://www.alphasoft.co.id/',
    'images':  ['images/main_screenshot.png'],
    'depends' : ['account', 'sale_management', 'purchase', 'stock'],
    'data': [
        'security/ir_group.xml',
        'security/ir.model.access.csv',
        # 'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/picking_views.xml',
        'views/stock_production_lot_views.xml',
        'views/account_move_views.xml',
    ],
    'demo': [],
    'test': [],
    'qweb': [],
    'css': [],
    'js': [],
    'price': 15.00,
    'currency': 'EUR',
    'installable': True,
    'application': False,
    'auto_install': False,
}
