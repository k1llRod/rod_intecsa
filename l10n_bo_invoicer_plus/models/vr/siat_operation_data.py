from odoo import api, fields, models


class SiatOperationData(models.Model):
    _name = "siat.operation.data"

    vr_server = fields.Char(
        string='Servidor Versatil',
    )

    vr_api_key = fields.Char(
        string='API KEY',
    )

    vr_codigo_sucursal = fields.Integer(
        string='Código Sucursal',
    )

    vr_codigo_pos = fields.Integer(
        string='Código Punto de Venta',
    )

    vr_cuis = fields.Char(
        string='CUIS',
    )

    vr_codigo_ambiente = fields.Integer(
        string='Código Ambiente',
    )

    vr_nit_emisor = fields.Integer(
        string='NIT Emisor',
    )

    vr_modalidad_facturacion = fields.Integer(
        string='Modalidad Facturación',
    )

    vr_tipo_factura = fields.Integer(
        string='ID Tipo Factura',
    )

    vr_tipo_factura_descripcion = fields.Char(
        string='Descripción Tipo Factura',
    )

    vr_tipo_documento_sector = fields.Integer(
        string='ID Tipo Documento Sector',
    )

    vr_leyenda = fields.Char(
        string='Leyenda',
    )

    vr_numero_factura = fields.Integer(
        string='Número de Factura',
    )

    vr_es_casa_matriz = fields.Boolean(
        string='Es Casa Matriz',
    )

    vr_direccion = fields.Char(
        string='Dirección Emisor',
    )

    vr_telefono = fields.Char(
        string='Teléfono Emisor',
    )

    vr_municipio = fields.Char(
        string='Municipio Emisor',
    )

    vr_cufd_id = fields.Integer(
        string='ID CUFD actual',
    )

    vr_cufd_codigo_control = fields.Char(
        string='CUFD Código Control',
    )

    vr_send_invoice_data = fields.Boolean(
        string='Grupo Datos Factura activado',
    )

    vr_send_cuis_data = fields.Boolean(
        string='Grupo Datos CUIS activado',
    )

    vr_send_user_data = fields.Boolean(
        string='Grupo Datos Usuario activado',
    )

    vr_send_amounts = fields.Boolean(
        string='Grupo Montos activado',
    )

    vr_send_qr = fields.Boolean(
        string='Envio de QR activado',
    )

    vr_client_sends_invoice_number = fields.Boolean(
        string='El Cliente envía el número de factura',
    )