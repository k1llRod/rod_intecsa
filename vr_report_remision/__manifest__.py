# -*-encoding: utf-8 -*-
#
# module written to Odoo,Open Source Management SOlution

# Developer(s): Ulises Atilano Gomez
# (ulises.atilano.g91@outlook.com)
{
    'name': 'Reporte de Remisiones',
    'version': '14.0.0.0',
    'author': 'VERSATIL SRL',
    'summary': 'SProduct Certifications',
    'description': """Remisiones Reporte""",
    'category': 'Base',
    'website': 'http://www.versatil.com.bo',
    'license': 'AGPL-3',
    'depends': [
        'sale_management',
        'base',
        'stock',
        'account',
        'sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/saleorder_report.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
}
