from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _prepare_invoice(self):
        ret = super(SaleOrder, self)._prepare_invoice()
        ret['vr_warehouse_id'] = self.warehouse_id.id
        ret['vr_razon_social'] = self.partner_invoice_id.vr_razon_social or self.partner_id.vr_razon_social
        ret['vr_nit_ci'] = self.partner_invoice_id.vat or self.partner_id.vat
        ret['vr_extension'] = self.partner_invoice_id.vr_extension or self.partner_id.vr_extension
        ret['vr_tipo_documento_identidad'] = self.partner_invoice_id.vr_tipo_documento_identidad or self.partner_id.vr_tipo_documento_identidad
        ret['vr_metodo_pago'] = self.warehouse_id.vr_metodo_pago or False
        return ret

