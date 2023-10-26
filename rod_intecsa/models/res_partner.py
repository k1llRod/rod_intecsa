from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit ='res.partner'

    class_partner = fields.Selection([('class_a', 'Clase A'),
                                      ('class_b', 'Clase B'),
                                      ('class_c', 'Clase C')], string='Clase de contacto', compute='_compute_class_partner', store=True)
    reassigned = fields.Boolean(string='Reasignado', default=False)
    country_id = fields.Many2one('res.country', string='País', default=29)
    @api.depends('category_id')
    def _compute_class_partner(self):
        for record in self:
            if record.category_id:
                record.class_partner = record.category_id[-1].class_partner
            else:
                record.class_partner = False
    def assign_client(self):
        record_id = self.id
        # context = {
        #     'default_partner_payroll_id': record_id,
        #     'default_capital_base': self.capital_base,
        # }
        return {
            'name': 'Conciliar pagos de aportes',
            'type': 'ir.actions.act_window',
            'res_model': 'init.payroll.partner',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            # 'context': context,
        }