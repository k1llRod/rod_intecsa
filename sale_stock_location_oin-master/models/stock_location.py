# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 Eagle IT now <http://www.eagle-erp.com/>
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from eagle import models, fields, api, _


class StockLocation(models.Model):
    _inherit = 'stock.location'

    def name_get(self):
        """ Display product quantity along with location name """
        res = super(StockLocation, self).name_get()
        locations = []
        if self._context.get('product', False):
            for location in res:
                quant_ids = self.env['stock.quant'].search([('location_id', '=', location[0]),
                                                            ('product_id', '=', self._context['product']),
                                                            ('location_id.usage', '=', 'internal')])
                quantity = sum([quant.quantity - quant.reserved_quantity for quant in quant_ids])
                locations.append((location[0], str(quantity or 0.0) + ' ' + str(location[1])))
            return locations
        return res
