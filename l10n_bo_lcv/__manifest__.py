# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'LCV Impuestos Bolivia',
    'version': '13.0.0.1',
    'summary': 'Libro de compras, ventas y bancarización',
    'sequence': 30,
    'author': 'Franklin Justiniano',
    'description': """
    """,
    'category': 'Facturación Bolivia',
    'website': '',
    'images': [],
    'depends': ['l10n_bo_invoice', 'stock', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'views/lcv_impuestos_view.xml',
        'wizard/lcv_export_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}