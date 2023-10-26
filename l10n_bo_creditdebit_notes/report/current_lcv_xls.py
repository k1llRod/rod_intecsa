# -*- coding: utf-8 -*-
import datetime
import calendar
from odoo import models


class LcvReportXlsdc(models.AbstractModel):
    _name = 'report.l10n_bo_creditdebit_notes.lcv_report_xlsdc.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def get_lines(self, object):
        lines = []
        days = calendar.monthrange(int(object.year), int(object.period))
        date_init = datetime.date(year=int(object.year), month=int(object.period), day=1)
        date_end = datetime.date(year=int(object.year), month=int(object.period), day=int(days[1]))
        invoices = self.env['account.move'].search(
            [('invoice_date', '>=', date_init),
             ('invoice_date', '<=', date_end), ('state', 'in', ['posted']), ('move_type', '=', 'in_refund'),
             ('state_sin', 'in', ['V']), ('note_credit_debit', '=', True)], order="n_debitcredit ASC")

        valor = 1
        for invoice in invoices:
            vals = {
                'number_file': valor,
                'invoice_date': invoice.invoice_date,
                'n_debitcredit': invoice.n_debitcredit or '',
                'n_autorizacion': invoice.n_autorizacion or '',
                'nit_ci': invoice.nit_ci or '',
                'razon_social': invoice.razon_social or '',
                'amount_open': invoice.amount_open,
                'amount_iva': invoice.amount_iva,
                'codigo_control': invoice.codigo_control,
                'date_debitcredit': invoice.date_debitcredit,
                'n_factura': invoice.n_factura or '',
                'n_autorizacion_dc': invoice.n_autorizacion_dc,
                'amount_debitcredit': invoice.amount_debitcredit,
            }
            valor += 1
            lines.append(vals)
        return lines

    def generate_xlsx_report(self, workbook, data, object):

        sheet = workbook.add_worksheet('Notas Débito Crédito')

        format1 = workbook.add_format(
            {'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'vcenter',
             'bold': True})
        format10_2 = workbook.add_format(
            {'font_size': 10, 'align': 'right'})
        format10_3 = workbook.add_format(
            {'font_size': 10, 'align': 'left'})
        format21 = workbook.add_format(
            {'font_size': 9, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True,
             'bold': False})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
        font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
        font_size_number_8 = workbook.add_format(
            {'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8, 'num_format': '#.##'})
        red_mark = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8,
                                        'bg_color': 'red'})
        justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12})
        format3.set_align('center')
        font_size_8.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')

        format21.set_align('center')
        format21.set_align('vcenter')

        cell_format1 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
        cell_format1.set_num_format('#,##0.00')
        sheet.set_row(5, 60)

        tam_col = [5, 5, 10, 10, 15, 5, 12, 25, 15, 15, 15, 15, 15, 15, 15, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
                   12, 12, 12, 12, 12, 12]


        sheet.set_column('A:A', tam_col[0])
        sheet.set_column('B:B', tam_col[1])
        sheet.set_column('C:C', tam_col[2])
        sheet.set_column('D:D', tam_col[3])
        sheet.set_column('E:E', tam_col[4])
        sheet.set_column('F:F', tam_col[5])
        sheet.set_column('G:G', tam_col[6])
        sheet.set_column('H:H', tam_col[7])
        sheet.set_column('I:I', tam_col[8])
        sheet.set_column('J:J', tam_col[9])
        sheet.set_column('K:K', tam_col[10])
        sheet.set_column('L:L', tam_col[11])
        sheet.set_column('M:M', tam_col[12])
        sheet.set_column('N:N', tam_col[13])
        sheet.set_column('O:O', tam_col[14])
        sheet.set_column('P:P', tam_col[15])
        sheet.set_column('Q:Q', tam_col[16])
        sheet.set_column('R:R', tam_col[17])
        sheet.set_column('S:S', tam_col[18])
        sheet.set_column('T:T', tam_col[19])

        sheet.merge_range('B3:C3', u'PERIODO:', format10_2)
        sheet.merge_range('D3:E3', u'AÑO:', format10_2)
        sheet.write('F3:F3', object.year, format10_3)
        sheet.write('I3:I3', u'MES', format10_2)
        sheet.write('J3:J3', object.period, format10_3)

        sheet.merge_range('B4:D4', u'NOMBRE O RAZÓN SOCIAL:', format10_2)
        sheet.merge_range('E4:G4', object.company_id.razon_social, format10_3)
        sheet.write('I4:I4', u'NIT:', format10_2)
        sheet.merge_range('J4:K4', object.company_id.nit_ci, format10_3)

        sheet.merge_range('F2:J2', 'NOTAS DE CRÉDITO - DÉBITO', format1)
        sheet.write(5, 0, u'ESPECIFICACION', format21)
        sheet.write(5, 1, u'N°', format21)
        sheet.write(5, 2, u'FECHA NOTA DE CREDITO - DEBITO', format21)
        sheet.write(5, 3, u'N° DE NOTA DE CREDITO - DEBITO', format21)
        sheet.write(5, 4, u'N° DE AUTORIZACION', format21)
        sheet.write(5, 5, u'NIT PROVEEDOR', format21)
        sheet.write(5, 6, u'NOMBRE O RAZON SOCIAL PROVEEDOR', format21)
        sheet.write(5, 7, u'IMPORTE TOTAL DE LA DEVOLUCION O RESCISION EFECTUADA', format21)
        sheet.write(5, 8, u'DEBITO FISCAL', format21)
        sheet.write(5, 9, u'CODIGO DE CONTROL DE LA NOTA DE CREDITO-DEBITO', format21)
        sheet.write(5, 10, u'FECHA FACTURA ORIGINAL', format21)
        sheet.write(5, 11, u'N° DE FACTURA ORIGINAL', format21)
        sheet.write(5, 12, u'N° DE AUTORIZACION FACTURA ORIGINAL', format21)
        sheet.write(5, 13, u'IMPORTE TOTAL FACTURA ORIGINAL', format21)

        prod_row = 6
        prod_col = 0
        get_line = self.get_lines(object)
        amount_total = 0
        amount_dc = 0
        amount_iva = 0
        for each in get_line:
            fecha = each['invoice_date'].strftime('%d/%m/%Y')
            fecha_debitcredit = each['date_debitcredit'].strftime('%d/%m/%Y')
            sheet.write(prod_row, prod_col, '7', font_size_number_8)
            sheet.write(prod_row, prod_col + 1, each['number_file'], font_size_8)
            sheet.write(prod_row, prod_col + 2, str(fecha), font_size_8)
            sheet.write(prod_row, prod_col + 3, each['n_debitcredit'], font_size_8)
            sheet.write(prod_row, prod_col + 4, each['n_autorizacion'], font_size_8)
            sheet.write(prod_row, prod_col + 5, each['nit_ci'], font_size_8)
            sheet.write(prod_row, prod_col + 6, each['razon_social'] or '0', font_size_8)
            sheet.write_number(prod_row, prod_col + 7, each['amount_open'], cell_format1)
            sheet.write_number(prod_row, prod_col + 8, each['amount_iva'], cell_format1)
            sheet.write(prod_row, prod_col + 9, each['codigo_control'], font_size_number_8)
            sheet.write(prod_row, prod_col + 10, str(fecha_debitcredit), font_size_8)
            sheet.write(prod_row, prod_col + 11, each['n_factura'] or '', font_size_8)
            sheet.write(prod_row, prod_col + 12, each['n_autorizacion_dc'] or '', font_size_number_8)
            sheet.write_number(prod_row, prod_col + 13, each['amount_debitcredit'], cell_format1)
            amount_total += float(each['amount_open'])
            amount_iva += float(each['amount_iva'])
            amount_dc += float(each['amount_debitcredit'])
            prod_row += 1
        prod_row = prod_row - 1
        sheet.write(prod_row + 1, 6, u'TOTAL', format21)
        sheet.write_number(prod_row + 1, 7, amount_total, cell_format1)
        sheet.write_number(prod_row + 1, 8, amount_iva, cell_format1)
        sheet.write_number(prod_row + 1, 13, amount_dc, cell_format1)
