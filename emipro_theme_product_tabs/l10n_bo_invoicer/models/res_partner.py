from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    vr_razon_social = fields.Char(
        string='Razón Social',
    )

    vr_tipo_documento_identidad = fields.Selection([
        ('1', 'CEDULA DE IDENTIDAD'),
        ('2', 'CEDULA DE IDENTIDAD DE EXTRANJERO'),
        ('3', 'PASAPORTE'),
        ('4', 'OTRO DOCUMENTO DE IDENTIDAD'),
        ('5', 'NÚMERO DE IDENTIFICACIÓN TRIBUTARIA'),
    ],
        string='Tipo de documento de Identidad',
        default='1',
        required=True,
    )

    vr_extension = fields.Char(
        string='Extensión',
    )

    # region AÑOS
    def get_years(self):
        year=1900
        years = []
        while year<=datetime.today().year:
            years.append((str(year), str(year)))
            year += 1
        return years
    # endregion

    vr_birthday_year = fields.Selection(
        get_years,
        string='Año',
    )

    # region MESES
    def get_months(self):
        return [
            ('1', 'enero'),
            ('2', 'febero'),
            ('3', 'marzo'),
            ('4', 'abril'),
            ('5', 'mayo'),
            ('6', 'junio'),
            ('7', 'julio'),
            ('8', 'agosto'),
            ('9', 'septiembre'),
            ('10', 'octubre'),
            ('11', 'noviembre'),
            ('12', 'diciembre'),
        ]
    # endregion

    vr_birthday_month = fields.Selection(
        get_months,
        string='Mes',
    )

    # region DIAS
    def get_days(self):
        day=1
        days = []
        while day<=24:
            days.append((str(day), str(day)))
            day += 1
        return days
    # endregion

    vr_birthday_day = fields.Selection(
        get_days,
        string='Dia',
    )

    vr_fecha_nacimiento = fields.Date(
        string='Fecha de Nacimiento',
    )

    # region ONCHANGE DIA, MES, AÑO
    @api.onchange('vr_birthday_day', 'vr_birthday_month', 'vr_birthday_year')
    def onchange_birthday(self):
        for res in self:
            if res.vr_birthday_day and res.vr_birthday_month and res.vr_birthday_year:
                birth = datetime.strptime(res.vr_birthday_year + '-' + res.vr_birthday_month + '-' + res.vr_birthday_day, '%Y-%m-%d').date()
                res.vr_fecha_nacimiento = birth
            else:
                res.vr_fecha_nacimiento = False
    # endregion

    @api.constrains('vr_birthday_day', 'vr_birthday_month', 'vr_birthday_year')
    def check_birthday(self):
        for res in self:
            if res.vr_birthday_day or res.vr_birthday_month or res.vr_birthday_year:
                if not res.vr_fecha_nacimiento:
                    raise ValidationError(_('La fecha de nacimiento esta incompleta.'))
