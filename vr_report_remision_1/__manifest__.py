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
        'report/report_landed_cost.xml',
        'report/report_landed_cost_template.xml',
        'reporte_remision_cliente_1.xml',
        'orden_de_pedido.xml',
        'fency_report_saleorder.xml',
        'views/sale_order_view.xml',
        'views/terms_views.xml',
        'views/saleorder_report.xml',
        'views/stock_picking.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
}
