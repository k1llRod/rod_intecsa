# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 Eagle IT now <http://www.eagle-erp.com/>
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from eagle import models, fields, api, _
from eagle.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def default_get(self, fields):
        res = super(SaleOrderLine, self).default_get(fields)
        if 'location_id' in fields and not res.get('location_id'):
            warehouse = self.env['stock.warehouse'].search(
                [('company_id', '=', self.env.user.company_id.id)], limit=1)
            res['location_id'] = warehouse and \
                warehouse.lot_stock_id.id or False
        return res

#     def _get_product_quantity(self):
#         quantity = 0.0
#         if self.product_id and self.location_id:
#             quant_ids = self.env['stock.quant'].search([('location_id', '=', self.location_id.id),
#                                                         ('product_id', '=', self.product_id.id),
#                                                         ('location_id.usage', '=', 'internal')])
#             quantity = sum([quant.quantity - quant.reserved_quantity for quant in quant_ids])
#         return quantity if quantity > 0 else 0.0

#     @api.depends('location_id', 'product_id', 'product_uom_qty')
#     def compute_available_qty(self):
#         for line in self:
#             if line.product_id:
#                 if not line.location_id:
#                     line.qty_available = line.product_id.qty_available
#                 else:
#                     line.qty_available = line._get_product_quantity()

    location_id = fields.Many2one('stock.location', string="Location",
                                  domain="[('usage','=','internal')]")
#     qty_available = fields.Float(compute=compute_available_qty,
#                                  string='Available Qty', store=True)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.constrains('order_line')
    def _check_product_location(self):
        for order in self:
            for line in order.order_line.filtered(lambda l:l.location_id):
                lines_count = line.search_count(
                    [('order_id', '=', order.id),
                     ('product_id', '=', line.product_id.id),
                     ('location_id', '=', line.location_id.id)])
                if lines_count > 1:
                    raise ValidationError(
                        _("""You cannot add same product %s with the same location %s .""" % (
                            line.product_id.display_name,
                            line.location_id.display_name)))


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(
            self, product_id, product_qty, product_uom, location_id,
            name, origin, company_id, values):
        if values.get('sale_line_id', False):
            sale_line_id = self.env['sale.order.line'].sudo().browse(
                values['sale_line_id'])
            if sale_line_id.location_id:
                self.location_src_id = sale_line_id.location_id.id
            else:
                self.location_src_id = self.picking_type_id.default_location_src_id.id
        return super(StockRule, self)._get_stock_move_values(
            product_id, product_qty, product_uom, location_id,
            name, origin, company_id, values)
