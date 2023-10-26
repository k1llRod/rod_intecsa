# -*- coding: utf-8 -*-
{
    'name': "agrupador productos",

    'summary': """
        Agrupación de productos para la factura""",

    'description': """
        Agrupación de productos para la factura
    """,

    'author': "versatil srl",
    'website': "http://www.versatil.com.bo",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/inherit_sale_order_view.xml',
        'views/grouped_products_view.xml',
        'views/inherit_account_move_view.xml',
        'views/invoice_report.xml',
    ],
}
