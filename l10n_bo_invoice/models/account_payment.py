from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    amount_pay = fields.Monetary(string="Monto Pagado")
    amount_change = fields.Monetary(string="Cambio")

    @api.onchange('amount_pay', 'amount')
    def _onchange_amount_pay(self):
        for payment in self:
            if payment.amount > 0:
                payment.amount_change = payment.amount_pay - payment.amount