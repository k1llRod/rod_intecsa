from odoo import models, fields, api, _

class PartnerCategory(models.Model):
    name ='partner.category'

    name = fields.Char(string='Category Name', required=True)
    description = fields.Text(string='Description')
    type = fields.Selection([('class_a', 'Clase A'),
                             ('class_b', 'Clase B')
                             ('class_c', 'Clase C')], string='Tipo de Cliente')
