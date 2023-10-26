from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    n_debitcredit = fields.Float(string='Nro. Nota Débito-Crédito', digits=(15, 0), default=0, copy=False)
    date_debitcredit = fields.Date(string='Fecha Fact. Original', copy=False)
    n_autorizacion_dc = fields.Char(string='N° Aut. Fact. Original', copy=False, help='Número de autorizacion Factura Original')
    amount_debitcredit = fields.Monetary(string='Total Factura Original',
                                 currency_field='',
                                 help='Importe Origina Factura Original')
