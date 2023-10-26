from odoo import fields, api, models, _
from odoo.exceptions import ValidationError


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    vr_codigo_sucursal = fields.Selection([
        ('0', 'Casa Matriz'),
        ('1', 'Sucursal 1'),
        ('2', 'Sucursal 2'),
        ('3', 'Sucursal 3'),
        ('4', 'Sucursal 4'),
        ('5', 'Sucursal 5'),
        ('6', 'Sucursal 6'),
        ('7', 'Sucursal 7'),
        ('8', 'Sucursal 8'),
        ('9', 'Sucursal 9'),
        ('10', 'Sucursal 10'),
        ('11', 'Sucursal 11'),
        ('12', 'Sucursal 12'),
        ('13', 'Sucursal 13'),
        ('14', 'Sucursal 14'),
        ('15', 'Sucursal 15'),
        ('16', 'Sucursal 16'),
        ('17', 'Sucursal 17'),
        ('18', 'Sucursal 18'),
        ('19', 'Sucursal 19'),
        ('20', 'Sucursal 20'),
    ],
        string='Código Sucursal',
    )

    def _get_payment_methods(self):
        return self.env['vr.prepare.data'].get_payment_methods()

    vr_metodo_pago = fields.Selection(
        selection=_get_payment_methods,
        string='Método de Pago',
        default='1',
    )

    vr_tipo_moneda = fields.Selection([
        ('1', 'Bolivianos'),
        ('2', 'Dólares'),
        ('7', 'Euros'),
    ],
        string='Tipo de Moneda',
        default='1',
    )

    @api.model
    def create(self, vals_list):
        # VALIDAR CÓDIGO SUCURSAL EXISTENTE
        self.check_exists_vr_codigo_sucursal(vals_list)
        res = super(StockWarehouse, self).create(vals_list)
        return res

    def write(self, vals):
        self.check_exists_vr_codigo_sucursal(vals)
        res = super(StockWarehouse, self).write(vals)
        return res

    def check_exists_vr_codigo_sucursal(self, vals):
        if 'vr_codigo_sucursal' in vals:
            find = self.env['stock.warehouse'].search([('vr_codigo_sucursal', '=', vals['vr_codigo_sucursal'])])
            if find:
                raise ValidationError(_('Ya existe una sucursal con el Código Sucursal SIAT %s', vals['vr_codigo_sucursal']))