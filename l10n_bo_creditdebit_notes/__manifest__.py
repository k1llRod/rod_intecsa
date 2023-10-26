# -*- coding: utf-8 -*-
{
    'name': "l10n_bo_creditdebit_notes",

    'summary': """
        Bolivia - Notas de Debito-Crédito""",

    'description': """
        Módulo localización para Bolivia
    """,

    'author': "Carlos N. López Fernández", "Franklin Justiniano"
                                           'website': "https://versatil.odoo.com/",

    'category': 'SIN',
    'version': '14.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'l10n_bo_invoice', 'l10n_bo_lcv', 'report_xlsx'],

    # always loaded
    'data': [
        'views/account_move_view.xml',
        'wizard/lcv_export_view.xml',
        'security/ir.model.access.csv',
    ]
}
