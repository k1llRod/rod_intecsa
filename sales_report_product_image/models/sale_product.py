# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    print_image = fields.Boolean(
        "Print Image",
        help="""If ticked, you can see the product image in
        report of sale order/quotation""",
    )
    image_sizes = fields.Selection(
        [
            ("image", "Big sized Image"),
            ("image_medium", "Medium Sized Image"),
            ("image_small", "Small Sized Image"),
        ],
        "Image Sizes",
        default="image_small",
        help="Image size to be displayed in report",
    )


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    #image_small = fields.Binary("Product Image", default="_get_default_image")

    #def _get_default_image(self):
	 #image_path = modules.get_module_resource('product_id.image_1920')
    #return tools.image_resize_image_big(base64.b64encode(open(image_path, 'rb').read()))
    image_small = fields.Binary("Product Image", related="product_id.image_1920", store="False")
