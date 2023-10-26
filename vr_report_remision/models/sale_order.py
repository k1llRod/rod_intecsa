# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
import locale
from .amount_to_literal import to_word


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.constrains('order_line')
    def _compute_amounts(self):
        amount_open = 0
        amount_des = 0
        for line in self:
            for line_inv in line.order_line:
                if line_inv.price_unit > 0:
                    amount_open += line_inv.product_uom_qty * line_inv.price_unit
                else:
                    amount_des += line_inv.product_uom_qty * line_inv.price_unit

        self.amount_des = amount_des * -1
        self.amount_open = amount_open

    today_date = fields.Date(string='Fecha', default=fields.Date.context_today)

    total_to_word = fields.Char(compute='to_literal', readonly=True)

    hospital_id = fields.Many2one('res.partner', string='Hospital', readonly=True,states={'draft': [('readonly', False)]})
    terms_id = fields.Many2one('sale.terms', string='Condiciones de venta', readonly=True,states={'draft': [('readonly', False)]})
    doctor = fields.Many2one('res.partner', 'Médico', readonly=True,states={'draft': [('readonly', False)]})
    patient = fields.Many2one('res.partner', 'Paciente', readonly=True,states={'draft': [('readonly', False)]})
    amount_open = fields.Monetary(string='Total Factura',
                                  compute='_compute_amounts',
                                  readonly=True,
                                  default=0)
    amount_des = fields.Monetary('Descuento',
                                 compute='_compute_amounts',
                                 readonly=True,
                                 default=0)
    vr_contact = fields.Text(string='Contacto')

    @api.depends('amount_total')
    def to_literal(self):
        for d in self:
            d.total_to_word = to_word(self.amount_total)


class SaleOrder(models.Model):
    _name = 'sale.terms'
    _description = 'Condiciones de venta'

    name = fields.Char(string='Nombre')
