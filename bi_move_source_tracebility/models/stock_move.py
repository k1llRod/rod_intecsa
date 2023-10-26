# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round


class stock_move(models.Model):
	
    _inherit  = 'stock.move'

    partner_id  =  fields.Many2one('res.partner','Partner')
    resource_sales_id = fields.Many2one('sale.order','Sale Document')
    resource_purchase_id = fields.Many2one('purchase.order','Purchase Document')
    date_invoice = fields.Date('Fecha de Factura')

    @api.model
    def create(self,vals):
        res = super(stock_move,self).create(vals)
        if res.picking_id.partner_id:
           res.partner_id = res.picking_id.partner_id.id
        return res 

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        self.ensure_one()
        # apply putaway
        location_dest_id = self.location_dest_id._get_putaway_strategy(self.product_id).id or self.location_dest_id.id
        vals = {
            'move_id': self.id,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'location_id': self.location_id.id,
            'location_dest_id': location_dest_id,
            'picking_id': self.picking_id.id,
            'partner_id': self.partner_id.id,
            'resource_sales_id': self.resource_sales_id.id or self.sale_line_id.order_id.id,
            'resource_purchase_id':self.resource_purchase_id.id,
            'date_invoice': self.date_invoice,

        }
        if quantity:
            uom_quantity = self.product_id.uom_id._compute_quantity(quantity, self.product_uom, rounding_method='HALF-UP')
            uom_quantity_back_to_product_uom = self.product_uom._compute_quantity(uom_quantity, self.product_id.uom_id, rounding_method='HALF-UP')
            rounding = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            if float_compare(quantity, uom_quantity_back_to_product_uom, precision_digits=rounding) == 0:
                vals = dict(vals, product_uom_qty=uom_quantity)
            else:
                vals = dict(vals, product_uom_qty=quantity, product_uom_id=self.product_id.uom_id.id)
        if reserved_quant:
            vals = dict(
                vals,
                location_id=reserved_quant.location_id.id,
                lot_id=reserved_quant.lot_id.id or False,
                package_id=reserved_quant.package_id.id or False,
                owner_id =reserved_quant.owner_id.id or False,
            )
        return vals

