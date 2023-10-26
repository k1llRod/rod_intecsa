from odoo import models, fields, api, _

class ReassignCustomers(models.TransientModel):
    _name ='reassign.customers'
    _description = 'Reassign Customers'

    class_a = fields.Char(string='Clase A')
    class_b = fields.Char(string='Clase B')
    class_c = fields.Char(string='Clase C')

    def select_partner(self):
        a = 1



