from odoo import api, fields, models


class CuisSIAT(models.Model):
    _name = "cuis.siat"

    name = fields.Char(
        string='Nombre',
    )

    codigo_sucursal = fields.Char(
        string='Código Sucursal',
    )

    codigo_pos = fields.Char(
        string='Código POS',
    )

    cuis = fields.Char(
        string='CUIS',
    )