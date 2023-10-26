# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round


class stock_picking_line(models.Model):
	
    _inherit  = 'stock.move.line'

    partner_id  =  fields.Many2one('res.partner')
    resource_sales_id = fields.Many2one('sale.order','Sale Document')
    resource_purchase_id = fields.Many2one('purchase.order','Purchase Document')
    date_invoice = fields.Date('Fecha de Factura')
