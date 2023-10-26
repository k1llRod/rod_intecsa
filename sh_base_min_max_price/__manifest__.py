# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    'name': 'Minimum and Maximum Product Price Base | Set Product Minimum Price | Set Product Maximum Price',

    'author': 'Softhealer Technologies',

    "license": "OPL-1",

    'website': 'https://www.softhealer.com',

    'support': 'support@softhealer.com',

    'version': '14.0.2',

    'category': 'Sales',

    'summary': "Set Minimum Product Price Set Maximum Product Price Manage Product Pricelist Management Min Product Price Max Product Price POS Product Min Price POS Product Max Price Point Of Sale Product Min Price Point Of Sale Product Max Price Odoo",

    'description': """This module is useful to set minimum and maximum selling price for the product. "Minimum and Maximum Product Price Base" is the base module for the "Minimum and Maximum Product Price" modules.""",
    "depends": ["base_setup" ,"product"],
    "data": [

        'security/price_security.xml',
        'views/product_config.xml',
    ],
    "images": ["static/description/background.png", ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": 1,
    "currency": "EUR"
}
