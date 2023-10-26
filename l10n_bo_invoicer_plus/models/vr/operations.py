from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

import base64
import json
import requests


class VrOperations(models.Model):
    _name = "vr.operations"

    # OBTENER LA URL DEL SERVIDOR VERSATIL
    def get_url_base(self):
        url_base = self.env['ir.config_parameter'].sudo().get_param('vr_server')
        if not url_base:
            raise ValidationError(_('Debe configurar el "Servidor Versatil" en configuraciones generales.'))
        else:
            return url_base

    # OBTENER EL APIKEY
    def get_api_key(self):
        api_key = self.env.company.vr_api_key
        if not api_key:
            raise ValidationError(
                _('Debe configurar el "API KEY" en la compañia: %s.', self.env.company.name))
        else:
            return api_key

    # VERIFICAR SI l10n_bo_discount ESTA INSTALADO
    def check_l10n_bo_discount_installed(self):
        discount_installed = self.env['ir.module.module'].sudo().search([
            ('name', '=', 'l10n_bo_discount'),
            ('state', '=', 'installed')
        ])
        if not discount_installed:
            return True
        else:
            return False

    # OBTENER API URL Y HEADERS
    def prepare_url_and_headers(self, service='invoicer'):
        try:
            url = self.get_url_base()
            api_key = self.get_api_key()
            headers = {
                'Content-type': 'application/json',
                # 'API-KEY': api_key,
            }
            # FACTURACIÓN
            if service == 'invoicer':
                url += '/invoicer/send_invoice/' + api_key
            # FACTURACIÓN OFFLINE
            elif service == 'invoicer_offline':
                url += '/invoicer/send_invoice_offline/' + api_key
            # ANULACIÓN
            elif service == 'cancel_invoice':
                url += '/invoicer/cancel_invoice/' + api_key
            # VERIFICAR CONEXIÓN CON SIAT
            elif service == 'check_conn':
                url += '/invoicer/check_conn_siat/' + api_key
                headers = {}
            # OBTENER DATOS DE OPERACIÓN EN MODO OFFLINE PARA PUNTO DE VENTA
            elif service == 'get_operation_pos_data':
                url += '/invoicer/get_operation_data/' + api_key
                headers = {}
            # OBTENER PDF
            elif service == 'get_pdf':
                url += '/invoicer/get_pdf/' + api_key
                headers = {}
            # OBTENER XML
            elif service == 'get_xml':
                url += '/invoicer/get_xml/' + api_key
                headers = {}
            elif service == 'get_invoice_number':
                url += '/invoicer/get_invoice_number/' + api_key
                headers = {}
            return url, headers
        except Exception as error:
            raise ValidationError(_(str(error)))

    # VERIFICAR CONEXIÓN CON SIAT
    def check_connection_siat(self):
        try:
            url, headers = self.prepare_url_and_headers(service='check_conn')
            response = requests.get(url, headers=headers)
            response = json.loads(response.text)
            return response
        except Exception as error:
            return False

    def send_invoice_backend(self):
        try:
            obj_inv = self.env['account.move'].browse(self.env.context.get('invoice_id'))
            url, headers = self.prepare_url_and_headers(service='invoicer')
            use_native_discount = self.check_l10n_bo_discount_installed()
            data = self.env['vr.prepare.data'].prepare_data_for_invoice(obj_inv, use_native_discount)
            response = requests.post(url, json=data, headers=headers)
            response = json.loads(response.text)
            if response['estado'] == 200:
                numero_factura = response['datos_factura']['numero_factura'] if 'datos_factura' in response else response['numero_factura']
                obj_inv.vr_numero_factura = numero_factura
                obj_inv.vr_codigo_recepcion = response['codigo_recepcion']
                obj_inv.vr_link_factura = response['link']
                obj_inv.vr_estado = 'send'
            else:
                raise ValidationError(_(str(response['mensajes'][0])))
        except Exception as error:
            raise ValidationError(_(str(error)))

    def cancel_invoice(self, obj_inv=None, pos=False):
        try:
            url, headers = self.prepare_url_and_headers(service='cancel_invoice')
            data = self.env['vr.prepare.data'].prepare_data_for_cancellation(obj_inv=obj_inv, pos=pos)
            response = requests.post(url, json=data, headers=headers)
            response = json.loads(response.text)
            if response['estado'] == 200:
                return True
            else:
                raise ValidationError(_(str(response['mensajes'][0])))
        except Exception as error:
            raise ValidationError(_(str(error)))

    # OBTENER DATOS DE OPERACIÓN EN MODO OFFLINE PARA PUNTO DE VENTA
    def get_operation_pos_data(self, data):
        try:
            url, headers = self.prepare_url_and_headers(service='get_operation_pos_data')
            response = requests.post(url, json=data, headers=headers)
            response = json.loads(response.text)
            if response['estado'] == 200:
                return self.save_in_siat_operation_data(response['datos'])
            else:
                raise ValidationError(_(str(response['mensajes'][0])))
        except Exception as error:
            if isinstance(error, ValidationError):
                raise ValidationError(_('%s Contáctese con soporte técnico. ', str(error)))
            else:
                raise ValidationError(
                    _('No existe conexión con el servidor Versatil para la obtención de datos necesarios para la facturación.\nNo es posible iniciar el Punto de Venta.\nIntente nuevamente o comuníquese con soporte técnico.'))

    # GUARDAR DATOS DE OPERACION EN CLIENTE
    def save_in_siat_operation_data(self, response):
        try:
            self.env['siat.operation.data'].search([('vr_cuis', '=', response['cuis'])]).unlink()
            siat_operationd_data = self.env['siat.operation.data'].create({
                'vr_server': self.get_url_base(),
                'vr_api_key': self.get_api_key(),
                'vr_codigo_sucursal': response['codigo_sucursal'],
                'vr_codigo_pos': response['codigo_pos'],
                'vr_cuis': response['cuis'],
                'vr_codigo_ambiente': response['codigo_ambiente'],
                'vr_nit_emisor': response['nit_emisor'],
                'vr_modalidad_facturacion': response['modalidad_facturacion'],
                'vr_tipo_factura': response['tipo_factura'],
                'vr_tipo_factura_descripcion': response['tipo_factura_descripcion'],
                'vr_tipo_documento_sector': response['tipo_documento_sector'],
                'vr_leyenda': response['leyenda'],
                'vr_numero_factura': response['numero_factura'],
                'vr_es_casa_matriz': response['es_casa_matriz'],
                'vr_direccion': response['direccion'],
                'vr_telefono': response['telefono'],
                'vr_municipio': response['municipio'],
                'vr_cufd_id': response['cufd_id'],
                'vr_cufd_codigo_control': response['cufd_codigo_control'],
                'vr_send_invoice_data': response['send_invoice_data'],
                'vr_send_cuis_data': response['send_cuis_data'],
                'vr_send_user_data': response['send_user_data'],
                'vr_send_amounts': response['send_amounts'],
                'vr_send_qr': response['send_qr'],
                'vr_client_sends_invoice_number': response['client_sends_invoice_number'],
            })
            return siat_operationd_data
        except Exception as error:
            raise ValidationError(_(str(error)))

    # OBTENER FACTURA EN FORMATO PDF
    def get_pdf(self, obj_inv, type, pos=False):
        try:
            if obj_inv.vr_attachment_id_mp and type == 'media_pagina':
                attachment_id = obj_inv.vr_attachment_id_mp.id
            elif obj_inv.vr_attachment_id_rollo and type == 'rollo':
                attachment_id = obj_inv.vr_attachment_id_rollo.id
            else:
                url, headers = self.prepare_url_and_headers(service='get_pdf')
                data = self.env['vr.prepare.data'].prepare_data_for_get_pdf(obj_inv, type, pos)
                response = requests.post(url, json=data, headers=headers)
                if response:
                    # GUARDAR ARCHIVO EN ATTACHMENT
                    attachment = self.env['ir.attachment'].create({
                        'name': 'Factura_' + str(obj_inv.vr_numero_factura),
                        'datas': base64.b64encode(response.content),
                        'res_model': 'account.move' if not pos else 'pos.order',
                        'res_id': obj_inv.id,
                        'mimetype': 'application/pdf',
                        'type': 'binary',
                    })
                    # GUARDAR ARCHIVO EN LOCAL
                    if type == 'media_pagina':
                        obj_inv.vr_attachment_id_mp = attachment.id
                    elif type == 'rollo':
                        obj_inv.vr_attachment_id_rollo = attachment.id

                    attachment_id = attachment.id
                else:
                    raise ValidationError(
                        _('No es posible encontrar el reporte de tipo %s para esta factura.', type))
            return {
                'type': 'ir.actions.act_url',
                'name': '%s' % "factura_mp.pdf",
                'target': 'new',
                'url': '/web/content/%s?' % attachment_id,
            }
        except Exception as error:
            raise ValidationError(_(str(error)))

    # OBTENER FACTURA EN FORMATO XML
    def get_xml(self, obj_inv, pos=False):
        try:
            if obj_inv.vr_attachment_id_xml:
                attachment_id = obj_inv.vr_attachment_id_xml.id
            else:
                url, headers = self.prepare_url_and_headers(service='get_xml')
                data = self.env['vr.prepare.data'].prepare_data_for_get_xml(obj_inv, pos)
                response = requests.post(url, json=data, headers=headers)
                if response:
                    # GUARDAR ARCHIVO EN ATTACHMENT
                    attachment = self.env['ir.attachment'].create({
                        'name': 'Xml_' + str(obj_inv.vr_numero_factura),
                        'datas': base64.b64encode(response.content),
                        'res_model': 'account.move' if not pos else 'pos.order',
                        'res_id': obj_inv.id,
                        'mimetype': 'text/xml',
                        'type': 'binary',
                    })
                    # GUARDAR ARCHIVO EN LOCAL
                    obj_inv.vr_attachment_id_xml = attachment.id

                    attachment_id = attachment.id
                else:
                    raise ValidationError(
                        _('No es posible encontrar el xml para esta factura.'))
            return {
                'type': 'ir.actions.act_url',
                'name': '%s' % "xml.pdf",
                'target': 'new',
                'url': '/web/content/%s?download=1' % attachment_id,
            }
        except Exception as error:
            raise ValidationError(_(str(error)))
