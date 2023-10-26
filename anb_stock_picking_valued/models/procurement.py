# -*- coding: utf-8 -*-
################################################################
#    License, author and contributors information in:          #
#    __openerp__.py file at the root folder of this module.    #
################################################################

from odoo import models
import logging
_logger = logging.getLogger(__name__)


class ProcurementOrder(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self):
        ''' Returns a dictionary of values that will be used to create a stock
        move from a procurement. This function assumes that the given
        procurement has a rule (action == 'move') set on it.
        :param procurement: browse record
        :rtype: dictionary
        '''
        vals = super(ProcurementOrder, self)._get_stock_move_values()
        if self.sale_line_id:
            line = self.sale_line_id
            vals.update({
                'move_price_unit': line.price_unit,
                'price_subtotal': line.price_subtotal,
                'price_reduce': line.price_reduce,
                'tax_id': [(4, tax.id) for tax in line.tax_id],
                'discount': line.discount,
            })
        return vals
