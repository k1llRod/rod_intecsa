# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


{
    'name': ' Stock Move Traceability from Sales/purchase order receipt ',
    'version': '14.0.0.1',
    'category': 'Warehouse',
    'summary': 'stock Move Traceability for Sales Order product receipt on stock move so receipt on stock move so receipt on move lines receipt on stock move reference on stock move reference on move source document reference on move source document on stock move line',
    'description'	: """
          Move Traceability through Partner and Sales Order or Purchase Order Referance

    product receipt on stock move so receipt on stock move so receipt on move lines receipt on stock move
    reference on stock move reference on move source document reference on move 
    source document reference on stock move line reference on move lines
    odoo Goods receipt reference to stock transfer order receipt reference to stock transfer order
    odoo product reference to stock transfer order stock transfer order goods receipt reference to stock move
    odoo so receipt reference to stock move po receipt reference to stock moves line stock moves line reference
          
    



    """,
    'author': 'BrowseInfo',
    "price": 9.00,
    "currency": 'EUR',
    'website': 'https://www.browseinfo.in',
    
    'depends': ['base', 'sale_management', 'stock', 'sale_stock','purchase'],

    'data': [

             'views/stock_move.xml',
            ],
    'demo': [],
    'test': [
            ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'live_test_url': "https://youtu.be/liTB5ULFcIA",
    "images":['static/description/Banner.png'],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


