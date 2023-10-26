from odoo import models, fields, api, _

class ResUsers(models.Model):
    _inherit ='res.users'

    class_partner = fields.Selection([('class_a', 'Clase A'),
                                      ('class_b', 'Clase B'),
                                      ('class_c', 'Clase C')], string='Clase de contacto')