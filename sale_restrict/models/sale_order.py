# See LICENSE file for full copyright and licensing details.

from odoo import _, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        zero_price = [x.product_id.name
                      for x in self.order_line if x.price_unit > x.product_id.pro_max_sale_price or x.price_unit < x.product_id.pro_min_sale_price]

        if zero_price:
            message = _("Please specify unit price for "
                        "the following products:") + '\n'
            message += '\n'.join(map(str, zero_price))
            raise UserError(message.rstrip())
        return super(SaleOrder, self).action_confirm()
