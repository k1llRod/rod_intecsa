from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_discount = fields.Boolean(string="Activate Universal Discount",
                                     related='company_id.enable_discount',
                                     readonly=False)
    sales_discount_product = fields.Many2one('product.product', string="Items Descuento",
                                             related='company_id.sales_discount_product',
                                             readonly=False)
    purchase_discount_product = fields.Many2one('product.product',
                                                string="Items Descuento Compras",
                                                related='company_id.purchase_discount_product',
                                                readonly=False)