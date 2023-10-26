# Copyright 2014-2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from .amount_to_literal import to_word

class SaleOrder(models.Model):
    _inherit = "sale.order"

    vr_entrega = fields.Char(string="Fecha de Entrega")
    name_ent = fields.Char(string="N° de Entrega")
    #amount_text = fields.Char(string="Monto Literal")
    @api.depends('amount_total')
    def to_literal(self):
        for d in self:
            d.total_to_word = to_word(self.amount_total)

    total_to_word = fields.Char(compute='to_literal', readonly=True)

