# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round


class StockRule(models.Model):
    _inherit = 'stock.rule'
    
    
    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
        result = super(StockRule, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, company_id, values)
        
        result.update({
                'partner_id':values.get('partner_id',0),
                'resource_sales_id':values.get('resource_sales_id',0),
                'resource_purchase_id':values.get('resource_purchase_id',0),
                'date_invoice': values.get('date_invoice'),
            })
        return result