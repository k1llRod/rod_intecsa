from odoo import api, fields, models


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