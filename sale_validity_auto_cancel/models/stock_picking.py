###############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
###############################################################################
from datetime import datetime

from odoo import api, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def picking_auto_cancel(self):
        picking_ids = self.env['stock.picking'].search([
            ('state', '=', 'assigned'),
            ('scheduled_date', '<', datetime.now().strftime('%Y-%m-%d'))
        ])
        for order in picking_ids:
            order.action_cancel()
