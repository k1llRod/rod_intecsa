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


class LcvExportWizardDc(models.TransientModel):
    _name = "lcv.export.wizard.dc"

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

    def act_getfile(self):
        if self.format == 'xls':
            self.ensure_one()
            report_name = 'l10n_bo_creditdebit_notes.lcv_report_xlsdc.xlsx'
            return self.env['ir.actions.report'].search(
                [('report_name', '=', report_name),
                 ('report_type', '=', 'xlsx')], limit=1).report_action(self)
        else:
            this = self[0]
            days = calendar.monthrange(int(this.year), int(this.period))
            date_init = datetime.date(year=int(this.year), month=int(this.period), day=1)
            date_end = datetime.date(year=int(this.year), month=int(this.period), day=int(days[1]))
            invoice = self.env['account.move'].search(
                [('invoice_date', '>=', date_init),
                 ('invoice_date', '<=', date_end), ('state', 'in', ['posted']), ('move_type', '=', 'in_refund'),
                 ('state_sin', 'in', ['V']), ('note_credit_debit', '=', True)], order="n_debitcredit ASC")

            with contextlib.closing(io.BytesIO()) as buf:
                this.trans_export(invoice, buf, this.format, self._cr)
                out = base64.encodestring(buf.getvalue())

            filename = 'lcv_' + str(this.period) + '_' + str(this.year)
            extension = this.format
            name = "%s.%s" % (filename, extension)
            this.write({'state': 'get', 'data': out, 'name': name})
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'lcv.export.wizard.dc',
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
                number_file = 1
                for inv in rows:
                    fecha = inv.invoice_date.strftime('%d/%m/%Y')
                    fecha_debitcredit = inv.date_debitcredit.strftime('%d/%m/%Y')
                    writer.writerow((str('7'),
                                     str(number_file),
                                     str(fecha),
                                     str(int(inv.n_debitcredit)),
                                     str(inv.n_autorizacion or '0'),
                                     str(inv.nit_ci or '0'),
                                     str(inv.razon_social or ''),
                                     str(inv.amount_open),
                                     str(inv.amount_iva),
                                     str(inv.codigo_control or '0'),
                                     str(fecha_debitcredit),
                                     str(int(inv.n_factura)),
                                     str(inv.n_autorizacion_dc),
                                     str(inv.amount_debitcredit)
                                     ))

                    number_file = number_file + 1
            elif format == 'csv':
                writer = pycompat.csv_writer(buffer, delimiter=',',
                                             quotechar='|', quoting=csv.QUOTE_MINIMAL, dialect='UNIX')
                writer.writerow(("ESPECIFICACION",
                                 "N°",
                                 "FECHA NOTA DE CREDITO - DEBITO",
                                 "N° DE NOTA DE CREDITO - DEBITO",
                                 "N° DE AUTORIZACION",
                                 "NIT PROVEEDOR",
                                 "NOMBRE O RAZON SOCIAL PROVEEDOR",
                                 "IMPORTE TOTAL DE LA DEVOLUCION O RESCISION EFECTUADA",
                                 "DEBITO FISCAL",
                                 "CODIGO DE CONTROL DE LA NOTA DE CREDITO-DEBITO",
                                 "FECHA FACTURA ORIGINAL",
                                 "N° DE FACTURA ORIGINAL",
                                 "N° DE AUTORIZACION FACTURA ORIGINAL",
                                 "IMPORTE TOTAL FACTURA ORIGINAL"
                                 ))
                number_file = 1
                for inv in rows:
                    fecha = inv.invoice_date.strftime('%d/%m/%Y')
                    fecha_debitcredit = inv.date_debitcredit.strftime('%d/%m/%Y')
                    writer.writerow((str('7'),
                                     str(number_file),
                                     str(fecha),
                                     str(int(inv.n_debitcredit)),
                                     str(inv.n_autorizacion or '0'),
                                     str(inv.nit_ci or '0'),
                                     str(inv.razon_social or ''),
                                     str(inv.amount_open),
                                     str(inv.amount_iva),
                                     str(inv.codigo_control or '0'),
                                     str(fecha_debitcredit),
                                     str(int(inv.n_factura)),
                                     str(inv.n_autorizacion_dc),
                                     str(inv.amount_debitcredit)
                                     ))
                    number_file = number_file + 1


            else:
                raise Exception(_('Unrecognized extension: must be one of '
                                  '.csv, .po, or .tgz (received .%s).') % format)

        lines_inv = invoice
        _process(format, lines_inv, buffer)
        del lines_inv
