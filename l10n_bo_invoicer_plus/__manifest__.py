# -*- coding: utf-8 -*-
{
    'name': "Facturador Backend 2.0",
    'summary': """
        Facturación electrónica SIAT 2.0.""",
    'description': """
        Facturación electrónica SIAT 2.0.
    """,
    'author': "Carlos N. López Fernández",
    'website': "https://www.versatil.com.bo",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'product', 'account', 'stock', 'contacts','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/res_config_settings.xml',
        'views/res_partner.xml',
        'views/product_template.xml',
        'views/stock_warehouse.xml',
        'views/account_move.xml',
        'views/account_move_reversal_view.xml',
        'views/res_company.xml',
    ],
    'qweb': [
        'static/src/xml/card_number/vr_credit_card_widget.xml',
    ]
}
