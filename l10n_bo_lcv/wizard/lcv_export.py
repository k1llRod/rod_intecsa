# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import contextlib
import io
import csv

from odoo import api, fields, models, tools, _
import datetime
import calendar
from odoo.tools import config, pycompat, DEFAULT_SERVER_DATE_FORMAT

NEW_LANG_KEY = '__new__'


class LcvExportWizard(models.TransientModel):
    _name = "lcv.export.wizard"

    def _default_year(self):
        date = datetime.datetime.now()
        return date.year

    def _default_month(self):
        date = datetime.datetime.now()
        month = date.month - 1
        if month == 0:
            month = 12
        return str(month)

    name = fields.Char('Nombre de Archivo', readonly=True)
    format = fields.Selection([('csv', 'CSV'), ('txt', 'TXT'), ('xls', 'EXCEL')],
                              string='Formato de Archivo', required=True, default='txt')
    state = fields.Selection([('choose', 'choose'), ('get', 'get')],
                             default='choose')
    type = fields.Selection([('ventas', 'Ventas'), ('compras', 'Compras'), ('b_ventas', u'Bancarización Ventas'),
                             ('b_compras', u'Bancarización Compras')],
                            string='Tipo', required=True, default='ventas')
    warehouse_id = fields.Many2one('stock.warehouse', string=u'Sucursal')
    # dosificacion_id = fields.Many2one('dosing.control', string=u'Dosificación')
    dosificacion_id = fields.Many2many('dosing.control', 'dosing_lcv',
                                    'lcv_id', 'dosing_id',
                                    string=u'Dosificación')

    year = fields.Char(string=u'Año', default=_default_year)
    period = fields.Selection([('1', 'Enero'),
                               ('2', 'Febrero'),
                               ('3', 'Marzo'),
                               ('4', 'Abril'),
                               ('5', 'Mayo'),
                               ('6', 'Junio'),
                               ('7', 'Julio'),
                               ('8', 'Agosto'),
                               ('9', 'Septiembre'),
                               ('10', 'Octubre'),
                               ('11', 'Noviembre'),
                               ('12', 'Diciembre'), ], string=u'Periodo', default=_default_month)
    date_init = fields.Date(string=u'Desde fecha')
    date_end = fields.Date(string=u'A fecha')
    data = fields.Binary('File', readonly=True, attachment=False)
    company_id = fields.Many2one('res.company', string='Company', readonly=True,
                                 default=lambda self: self.env.user.company_id)
    all_sales = fields.Boolean(string='Todas las Sucursales y Dosificaciones', default=False)

    @api.onchange('dosificacion_id')
    def onchange_dosif(self):
        res = {}
        if self.type=='pos':
            res['domain'] = {'dosificacion_id': [('type', '=', 'pos')]}
        elif self.type!='pos':
            res['domain'] = {'dosificacion_id': [('type', '=', ['automatica','manual'])]}

        return res


    def act_getfile(self):
        if self.format == 'xls':
            self.ensure_one()
            report_name = 'l10n_bo_lcv.lcv_report_xls.xlsx'
            return self.env['ir.actions.report'].search(
                [('report_name', '=', report_name),
                 ('report_type', '=', 'xlsx')], limit=1).report_action(self)
        else:
            this = self[0]
            days = calendar.monthrange(int(this.year), int(this.period))
            warehouse_id = this.warehouse_id.id
            dosificacion_id = this.dosificacion_id.id
            date_init = datetime.date(year=int(this.year), month=int(this.period), day=1)
            date_end = datetime.date(year=int(this.year), month=int(this.period), day=int(days[1]))
            domain = []
            if dosificacion_id:
                domain = [('dosificacion', '=', dosificacion_id)]
            if this.type == 'ventas':
                invoice = self.env['account.move'].search(
                    [('warehouse_id', '=', warehouse_id), ('invoice_date', '>=', date_init),
                     ('invoice_date', '<=', date_end), ('state', 'in', ['posted']), ('move_type', '=', 'out_invoice'),
                     ('state_sin', 'in', ['A', 'V'])] + domain, order="n_autorizacion, n_factura ASC")
            elif this.type == 'compras':
                invoice = self.env['account.move'].search(
                    [('invoice_date', '>=', date_init),
                     ('invoice_date', '<=', date_end), ('state', 'in', ['posted']), ('move_type', '=', 'in_invoice'),
                     ('state_sin', 'in', ['V'])], order="n_autorizacion, n_factura ASC")

            with contextlib.closing(io.BytesIO()) as buf:
                this.trans_export(invoice, buf, this.format, self._cr)
                out = base64.encodestring(buf.getvalue())

            filename = 'lcv_' + this.type + '_' + str(this.period) + '_' + str(this.year)
            extension = this.format
            name = "%s.%s" % (filename, extension)
            this.write({'state': 'get', 'data': out, 'name': name})
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'lcv.export.wizard',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': this.id,
                'views': [(False, 'form')],
                'target': 'new',
            }

    def trans_export(self, invoice, buffer, format, cr):

        def _process(format, rows, buffer):
            this = self[0]
            if format == 'txt':
                writer = pycompat.csv_writer(buffer, delimiter='|',
                                             quotechar='|', quoting=csv.QUOTE_MINIMAL, dialect='UNIX')
                if this.type == 'ventas':

                    number_file = 1
                    for inv in rows:
                        fecha = inv.invoice_date.strftime('%d/%m/%Y')
                        writer.writerow((str('3'),
                                         str(number_file),
                                         str(fecha),
                                         str(int(inv.n_factura)),
                                         str(inv.n_autorizacion),
                                         str(inv.state_sin),
                                         str(inv.nit_ci or ''),
                                         str(inv.razon_social or ''),
                                         str(inv.amount_open),
                                         str(inv.amount_ice_iehd),
                                         str(inv.amount_exe),
                                         '0',
                                         str(inv.amount_open - inv.amount_ice_iehd - inv.amount_exe),
                                         str(inv.amount_des),
                                         str(inv.amount_open - inv.amount_ice_iehd - inv.amount_exe - inv.amount_des),
                                         str(inv.amount_iva),
                                         str(inv.codigo_control)
                                         ))

                        number_file = number_file + 1
                elif this.type == 'compras':
                    number_file = 1
                    for inv in rows:
                        fecha = inv.invoice_date.strftime('%d/%m/%Y')
                        writer.writerow((str('1'),
                                         str(number_file),
                                         str(fecha),
                                         str(inv.nit_ci),
                                         str(inv.razon_social or ''),
                                         str(int(inv.n_factura)),
                                         str(inv.n_dui or '0'),
                                         str(inv.n_autorizacion or '0'),
                                         str(inv.amount_open),
                                         str(inv.amount_exe),
                                         str(inv.amount_open - inv.amount_exe),
                                         str(inv.amount_des),
                                         str(inv.amount_open - inv.amount_exe - inv.amount_des),
                                         str(inv.amount_iva),
                                         str(inv.codigo_control or '0'),
                                         str(inv.tipo_com or '')
                                         ))

                        number_file = number_file + 1
            elif format == 'csv':
                writer = pycompat.csv_writer(buffer, delimiter=',',
                                             quotechar='|', quoting=csv.QUOTE_MINIMAL, dialect='UNIX')

                if this.type == 'ventas':

                    writer.writerow(("ESPECIFICACION", "NRO",
                                     "FECHA DE LA FACTURA", "N DE LA FACTURA",
                                     "N DE AUTORIZACION", "ESTADO",
                                     "NIT/CI CLIENTE", "NOMBRE O RAZON SOCIAL",
                                     "IMPORTE TOTAL DE LA VENTA", "IMPORTE ICE/IEHD/IPJ/TASAS/OTROS NO SUJETOS AL IVA",
                                     "EXPORTACIONES Y OPERACIONES EXENTAS", "VENTAS GRAVADAS A TASA CERO",
                                     "SUBTOTAL", "DESCUENTOS BONIFICACIONES Y REBAJAS SUJETAS AL IVA",
                                     "IMPORTE BASE PARA DEBITO FISCAL", "DEBITO FISCAL", "CODIGO DE CONTROL"))
                    number_file = 1
                    for inv in rows:
                        fecha = inv.invoice_date.strftime('%d/%m/%Y')
                        writer.writerow((str('3'),
                                         str(number_file),
                                         str(fecha),
                                         str(int(inv.n_factura)),
                                         str(inv.n_autorizacion),
                                         str(inv.state_sin),
                                         str(inv.nit_ci or ''),
                                         str(inv.razon_social or ''),
                                         str(inv.amount_open),
                                         str(inv.amount_ice_iehd),
                                         str(inv.amount_exe),
                                         '0',
                                         str(inv.amount_open - inv.amount_ice_iehd - inv.amount_exe),
                                         str(inv.amount_des),
                                         str(inv.amount_open - inv.amount_ice_iehd - inv.amount_exe - inv.amount_des),
                                         str(inv.amount_iva),
                                         str(inv.codigo_control)
                                         )
                                        )
                        number_file = number_file + 1
                elif this.type == 'compras':
                    writer.writerow(("ESPECIFICACION",
                                     "NRO",
                                     "FECHA DE LA FACTURA",
                                     "NIT PROVEEDOR",
                                     "NOMBRE Y APELLIDO/RAZON SOCIAL",
                                     "N° DE LA FACTURA",
                                     "N° DE DUI",
                                     "N° DE AUTORIZACIÓN",
                                     "IMPORTE TOTAL DE LA COMPRA",
                                     "IMPORTE NO SUJETO A CREDITO FISCAL",
                                     "SUBTOTAL",
                                     "DESCUENTOS BONIFICACIONES Y REBAJAS OBTENIDAS",
                                     "IMPORTE BASE PARA CRÉDITO FISCAL",
                                     "CRÉDITO FISCAL",
                                     "CODIGO DE CONTROL",
                                     "TIPO DE COMPRA"))
                    number_file = 1
                    for inv in rows:
                        fecha = inv.invoice_date.strftime('%d/%m/%Y')
                        writer.writerow((str('1'),
                                         str(number_file),
                                         str(fecha),
                                         str(inv.nit_ci),
                                         str(inv.razon_social or ''),
                                         str(int(inv.n_factura)),
                                         str(inv.n_dui or '0'),
                                         str(inv.n_autorizacion or '0'),
                                         str(inv.amount_open),
                                         str(inv.amount_exe),
                                         str(inv.amount_open - inv.amount_exe),
                                         str(inv.amount_des),
                                         str(inv.amount_open - inv.amount_exe - inv.amount_des),
                                         str(inv.amount_iva),
                                         str(inv.codigo_control or '0'),
                                         str(inv.tipo_com or '')
                                         ))
                        number_file = number_file + 1


            else:
                raise Exception(_('Unrecognized extension: must be one of '
                                  '.csv, .po, or .tgz (received .%s).') % format)

        lines_inv = invoice
        _process(format, lines_inv, buffer)
        del lines_inv
