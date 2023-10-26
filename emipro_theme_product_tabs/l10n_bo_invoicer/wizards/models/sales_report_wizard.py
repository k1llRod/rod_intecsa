from odoo import fields, models, api, _
from datetime import datetime

from odoo.exceptions import ValidationError

_months = [
    ('1', 'Enero'),
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
    ('12', 'Diciembre'),
]

_get_sucursales = [
    ('0', 'Sucursal 0'),
    ('1', 'Sucursal 1'),
    ('2', 'Sucursal 2'),
]

_get_puntos_de_venta = [
    ('1', 'POS 1'),
    ('2', 'POS 2'),
]


class SalesReportWizard(models.TransientModel):
    _name = "sales.report.wizard"

    def default_get(self, fields_list):
        res = super(SalesReportWizard, self).default_get(fields_list)
        if res:
            cuis_list = self.env['vr.operations'].get_cuis_list()
            self.env['cuis.siat'].sudo().search([]).unlink()
            for cuis in cuis_list:
                self.save_cuis_siat(cuis)
        return res

    def save_cuis_siat(self, data):
        self.env['cuis.siat'].create({
            'name': data['nombre_sucursal'] if data['codigo_pos'] == 0 else data['nombre_pos'],
            'codigo_sucursal': str(data['codigo_sucursal']),
            'codigo_pos': str(data['codigo_pos']),
            'cuis': data['cuis'],
        })

    year = fields.Integer(
        string='Año',
        default=datetime.now().year,
        required=True,
    )

    month = fields.Selection(
        selection=_months,
        string='Periodo',
        default=str(datetime.now().month)
    )

    warehouse_m2o_id = fields.Many2one(
        comodel_name='cuis.siat',
        string='Sucursal',
        domain=[('codigo_pos', '=', '0')],
        ondelete='cascade',
    )

    pos_m2m_ids = fields.Many2many(
        comodel_name='cuis.siat',
        relation='report_cuis_pos_rel',
        column1='rep_id',
        column2='cuis_id',
        string='Puntos de Venta',
        domain=[('codigo_pos', '!=', '0')],
        ondelete='cascade',
    )

    @api.onchange('warehouse_m2o_id')
    def onchange_warehouse_m2o_id(self):
        for res in self:
            res.pos_m2m_ids = False
            if res.warehouse_m2o_id:
                return {
                    'domain': {
                        'pos_m2m_ids': [
                            ('codigo_sucursal', '=', res.warehouse_m2o_id.codigo_sucursal),
                            ('codigo_pos', '!=', '0'),
                        ]
                    }
                }
            else:
                return {
                    'domain': {
                        'pos_m2m_ids': [('codigo_pos', '!=', '0')]
                    }
                }

    def get_report(self):
        try:
            vr_op = self.env['vr.operations']
            cuis_codes = []
            if self.warehouse_m2o_id:
                cuis_codes.append(self.warehouse_m2o_id.cuis)
            if self.pos_m2m_ids:
                cuis_codes += self.pos_m2m_ids.mapped('cuis')
            return vr_op.get_sales_report_excel(vr_op.dict2obj({
                'cuis_codes': cuis_codes,
                'year': self.year,
                'month': self.month
            }))
        except Exception as error:
            raise ValidationError(_(str(error)))
