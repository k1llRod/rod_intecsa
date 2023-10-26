# -*-encoding: utf-8 -*-
#
# module written to Odoo,Open Source Management SOlution

# Developer(s): Ulises Atilano Gomez
# (ulises.atilano.g91@outlook.com)

from odoo import fields, models, api
from odoo.addons.website import tools
from odoo.exceptions import UserError
from odoo.tools import pycompat, base64
from .amount_to_literal import to_word


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    today_date = fields.Date(string='Fecha', default=fields.Date.context_today)
    sale_id = fields.Many2one('sale.order', 'Sale Order')
    hospital_id = fields.Many2one('res.company', string='Hospital', index=True)
    terms_id = fields.Many2one('sale.terms', string='Condiciones de venta')

    currency_id = fields.Many2one(
        related="sale_id.currency_id",
        readonly=True,
        string="Currency",
        related_sudo=True,  # See explanation for sudo in compute method
    )
    amount_untaxed = fields.Monetary(
        compute="_compute_amount_all",
        string="Untaxed Amount",
        compute_sudo=True,  # See explanation for sudo in compute method
    )
    amount_tax = fields.Monetary(
        compute="_compute_amount_all", string="Taxes", compute_sudo=True
    )
    amount_total = fields.Monetary(
        compute="_compute_amount_all", string="Total", compute_sudo=True
    )

    total_to_word = fields.Char(compute='to_literal', readonly=True)

    @api.depends('amount_total')
    def to_literal(self):
        for d in self:
            d.total_to_word = to_word(self.amount_total)

    def _compute_amount_all(self):
        """This is computed with sudo for avoiding problems if you don't have
        access to sales orders (stricter warehouse users, inter-company
        records...).
        """
        for pick in self:
            round_curr = pick.sale_id.currency_id.round
            amount_tax = 0.0
            #for tax_group in pick.get_taxes_values().values():
            #    amount_tax += round_curr(tax_group["amount"])
            amount_untaxed = sum(l.sale_price_subtotal for l in pick.move_line_ids)
            pick.update(
                {
                    "amount_untaxed": amount_untaxed,
                    "amount_tax": amount_tax,
                    "amount_total": amount_untaxed + amount_tax,
                }
            )

    def get_taxes_values(self):
        tax_grouped = {}
        for line in self.move_line_ids:
            for tax in line.sale_line.tax_id:
                tax_id = tax.id
                if tax_id not in tax_grouped:
                    tax_grouped[tax_id] = {"base": line.sale_price_subtotal, "tax": tax}
                else:
                    tax_grouped[tax_id]["base"] += line.sale_price_subtotal
        for tax_id, tax_group in tax_grouped.items():
            tax_grouped[tax_id]["amount"] = tax_group["tax"].compute_all(
                tax_group["base"], self.sale_id.currency_id
            )["taxes"][0]["amount"]
        return tax_grouped







