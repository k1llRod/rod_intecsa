# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    tawk_id = fields.Char(string='Tawk.to Site ID')
