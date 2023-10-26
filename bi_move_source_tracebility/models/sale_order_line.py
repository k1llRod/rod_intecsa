# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'


    def _prepare_procurement_values(self,group_id):
        res = super(sale_order_line,self)._prepare_procurement_values(group_id=group_id)
        res.update({
            'partner_id':self.order_id.partner_id.id,
            'resource_sales_id': self.order_id.id,
            })
        return res
