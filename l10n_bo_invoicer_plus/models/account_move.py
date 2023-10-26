from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    vr_warehouse_id = fields.Many2one(
        comodel_name='stock.warehouse',
        string='Sucursal',
    )

    vr_razon_social = fields.Char(
        string='Razón Social',
        default='S/N',
    )

    vr_nit_ci = fields.Char(
        string='NIT/CI',
    )

    vr_extension = fields.Char(
        string='Extensión',
    )

    vr_tipo_documento_identidad = fields.Selection([
        ('1', 'CI - CEDULA DE IDENTIDAD'),
        ('2', 'CEX - CEDULA DE IDENTIDAD DE EXTRANJERO'),
        ('3', 'PAS - PASAPORTE'),
        ('4', 'OD - OTRO DOCUMENTO DE IDENTIDAD'),
        ('5', 'NIT - NÚMERO DE IDENTIFICACIÓN TRIBUTARIA'),
    ],
        string='Tipo Documento Identidad',
    )

    vr_codigo_motivo = fields.Integer(
        string='Motivo de Anulación',
    )

    def _get_payment_methods(self):
        return self.env['vr.prepare.data'].get_payment_methods()

    vr_metodo_pago = fields.Selection(
        selection=_get_payment_methods,
        string='Código Método de Pago SIAT',
    )

    vr_nro_tarjeta = fields.Char(
        string='Número tarjeta',
        compute='build_nro_tarjeta',
        store=False,
        copy=False,
    )

    vr_nro_tarjeta_1 = fields.Char(copy=False, default='',)
    vr_nro_tarjeta_2 = fields.Char(copy=False, default='',)
    vr_nro_tarjeta_3 = fields.Char(copy=False, default='',)
    vr_nro_tarjeta_4 = fields.Char(copy=False, default='',)
    vr_nro_tarjeta_5 = fields.Char(copy=False, default='',)
    vr_nro_tarjeta_6 = fields.Char(copy=False, default='',)
    vr_nro_tarjeta_7 = fields.Char(copy=False, default='',)
    vr_nro_tarjeta_8 = fields.Char(copy=False, default='',)

    vr_is_card = fields.Boolean(
        string='Pago con tarjeta',
        compute='check_is_card',
    )

    vr_numero_factura = fields.Integer(
        string='Número Factura',
        copy=False,
    )

    vr_codigo_recepcion = fields.Char(
        string='Código Recepción Factura',
        copy=False,
    )

    vr_link_factura = fields.Char(
        string='Link SIAT',
        copy=False,
    )

    vr_estado = fields.Selection([
        ('send', 'Enviado'),
        ('cancelled', 'Anulado'),
    ],
        string='Estado SIAT',
        copy=False,
    )

    vr_attachment_id_xml = fields.Many2one(
        comodel_name='ir.attachment',
        string='Archivo XML',
        help='Archivo XML Factura.',
        copy=False,
    )

    vr_attachment_id_mp = fields.Many2one(
        comodel_name='ir.attachment',
        string='Archivo MP',
        help='Archivo PDF Factura (Media Página).',
        copy=False,
    )

    vr_attachment_id_rollo = fields.Many2one(
        comodel_name='ir.attachment',
        string='Archivo Rollo',
        help='Archivo PDF Factura (Rollo).',
        copy=False,
    )

    vr_send_to_middleware = fields.Boolean(
        string='Enviar Factura a Servidor Versatil',
        default=True,
        copy=False,
    )

    # CONCATENAR NÚMERO DE TARJETA
    @api.depends('vr_nro_tarjeta_1', 'vr_nro_tarjeta_2', 'vr_nro_tarjeta_3', 'vr_nro_tarjeta_4', 'vr_nro_tarjeta_5',
                 'vr_nro_tarjeta_6',
                 'vr_nro_tarjeta_7', 'vr_nro_tarjeta_8')
    def build_nro_tarjeta(self):
        for res in self:
            res.vr_nro_tarjeta = str(res.vr_nro_tarjeta_1) + str(res.vr_nro_tarjeta_2) + str(
            res.vr_nro_tarjeta_3) + str(
            res.vr_nro_tarjeta_4) + str(res.vr_nro_tarjeta_5) + str(res.vr_nro_tarjeta_6) + str(
            res.vr_nro_tarjeta_7) + str(
            res.vr_nro_tarjeta_8)

    # VERIFICAR SI EL MÉTODO DE PAGO SELCCIONADO ES DE TIPO 'TARJETA'
    @api.depends('vr_metodo_pago')
    def check_is_card(self):
        for res in self:
            if self.find_for_card_in_metodos_pago():
                res.vr_is_card = True
            else:
                res.vr_is_card = False
                res.vr_nro_tarjeta_1 = ""
                res.vr_nro_tarjeta_2 = ""
                res.vr_nro_tarjeta_3 = ""
                res.vr_nro_tarjeta_4 = ""
                res.vr_nro_tarjeta_5 = ""
                res.vr_nro_tarjeta_6 = ""
                res.vr_nro_tarjeta_7 = ""
                res.vr_nro_tarjeta_8 = ""
                res.vr_nro_tarjeta = False

    def find_for_card_in_metodos_pago(self):
        if self.vr_metodo_pago:
            value = list(filter(lambda x: self.vr_metodo_pago in x, self._get_payment_methods()))[0][1]
            if value.find("TARJETA") != -1:
                return True
            else:
                return False
        else:
            return False

    # ESTABLECER VALORES AL SELECCIONAR PARTNER_ID
    @api.onchange('partner_id')
    def vr_onchange_partner_id(self):
        for res in self:
            res.vr_razon_social = res.partner_id.vr_razon_social or 'S/N'
            res.vr_nit_ci = res.partner_id.vat
            res.vr_extension = res.partner_id.vr_extension
            res.vr_tipo_documento_identidad = res.partner_id.vr_tipo_documento_identidad

    # ESTABLECER VALORES AL SELECCIONAR VR_WAREHOUSE_ID
    @api.onchange('vr_warehouse_id')
    def vr_onchange_vr_warehouse_id(self):
        for res in self:
            res.vr_metodo_pago = res.vr_warehouse_id.vr_metodo_pago

    # ENVIAR FACTURA
    def action_post(self):
        res = super(AccountMove, self).action_post()
        # FACTURAR SIAT
        if self.move_type == 'out_invoice' and self.vr_send_to_middleware:
            self.env['vr.operations'].with_context({'invoice_id': self.id}).send_invoice_backend()
        return res

    # OBTENER FACTURA EN PDF (media página o rollo)
    def vr_get_mp_pdf(self):
        return self.vr_get_pdf('media_pagina')

    def vr_get_rollo_pdf(self):
        return self.vr_get_pdf('rollo')

    def vr_get_pdf(self, type):
        if not self:
            self = self.env['account.move'].browse(self.env.context.get('active_id'))
        return self.env['vr.operations'].get_pdf(obj_inv=self, type=type)

    def vr_get_xml(self):
        if not self:
            self = self.env['account.move'].browse(self.env.context.get('active_id'))
        return self.env['vr.operations'].get_xml(obj_inv=self)
