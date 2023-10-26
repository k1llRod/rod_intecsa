# -*- coding: utf-8 -*-

{
    'name': 'Website Add Tawk.to',
    'version': '1.0',
    'category': 'website',
    'sequence': 6,
    'author': 'ErpMstar Solutions',
    'summary': 'This module allows you to add Tawk.to in your Odoo website.',
    'description': "This module allows you to add Tawk.to in your Odoo website.",
    'depends': ['website'],
    'data': [
        'views/template.xml',
        'views/views.xml',
    ],
    'qweb': [

    ],
    'images': [
        'static/description/web.jpg',
    ],
    'installable': True,
    'website': '',
    'auto_install': False,
    'price': 9,
    'currency': 'EUR',
}
