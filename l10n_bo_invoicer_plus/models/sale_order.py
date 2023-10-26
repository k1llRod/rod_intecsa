from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _prepare_invoice(self):
        ret = super(SaleOrder, self)._prepare_invoice()
        ret['vr_warehouse_id'] = self.warehouse_id.id
        ret['vr_razon_social'] = self.partner_id.vr_razon_social
        ret['vr_nit_ci'] = self.partner_id.vat
        ret['vr_extension'] = self.partner_id.vr_extension
        ret['vr_tipo_documento_identidad'] = self.partner_id.vr_tipo_documento_identidad
        return ret

