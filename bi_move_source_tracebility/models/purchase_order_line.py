# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round

class purchase_order(models.Model):

    _inherit = 'purchase.order.line'

    def _create_stock_moves(self, picking):
       moves = self.env['stock.move']
       done = self.env['stock.move'].browse()
       for line in self:
           for val in line._prepare_stock_moves(picking):
               val.update({
			             'partner_id':line.order_id.partner_id.id,
                         'resource_purchase_id':line.order_id.id,
                         'date_invoice': line.order_id.date_invoice,
					})
				
               done += moves.create(val)
       return done
