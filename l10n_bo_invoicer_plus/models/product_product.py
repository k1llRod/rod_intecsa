from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = "product.product"

    # vr_tipo_nombre_producto = fields.Selection([
    #     ('internal', 'Referencia Interna'),
    #     ('barcode', 'Código de Barras'),
    # ],
    #     string='Usar como nombre de Producto',
    # )

    # vr_nombre_producto = fields.Char(
    #     string='Nombre Producto',
    #     compute='_vr_compute_nombre_producto',
    #     store=True,
    # )
    #
    # @api.depends('vr_tipo_nombre_producto')
    # def _vr_compute_nombre_producto(self):
    #     for res in self:
    #         if res.vr_tipo_nombre_producto == 'internal':
    #             res.vr_nombre_producto = res.default_code
    #         elif res.vr_tipo_nombre_producto == 'barcode':
    #             res.vr_nombre_producto = res.barcode
    #         else:
    #             res.vr_nombre_producto = False

    # @api.constrains('vr_nombre_producto')
    # def check_internal_reference_or_barcode(self):
    #     for res in self:
    #         if not res.default_code and res.vr_tipo_nombre_producto == 'internal':
    #             raise ValidationError(
    #                 _('Es necesario establecer la referencia interna del producto en la pestaña "Información General".'))
    #         elif not res.barcode and res.vr_tipo_nombre_producto == 'barcode':
    #             raise ValidationError(
    #                 _('Es necesario establecer el código barcode del producto en la pestaña "Información General".'))