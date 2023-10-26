# -*- coding: utf-8 -*-

{
    'name': 'Auto Product SKU Generator App',
    'author': 'Edge Technologies',
    'version': '14.0.1.1',
    'live_test_url': "https://youtu.be/k5974K7Q63I",
    'license':'OPL-1',
    'images':['static/description/main_screenshot.png'],
    'summary': 'Auto Generate internal reference for product code automatic product code generate auto product code auto product internal reference Generator product SKU automatic SKU Generator auto internal reference generate Product auto sku generate product code sku ',
    'description': """
        This app helps you to generate internal reference for products and it's variants,
        also generate internal reference automatically when creating new product.
    """,
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/main_window.xml',
        'data/sequence.xml',
    ],
    'installable': True,
    'auto_install': False,
    'price': 10,
    'currency': "EUR",
    'category': 'Sales'
}
