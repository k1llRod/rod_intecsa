from odoo import _, api, fields, models

class InheritAccountMove(models.Model):
    _inherit = 'account.move'

    grouped_products_ids = fields.One2many('vr.grouped_products', 'account_move_id')
    doctor = fields.Char(
        string='Médico',
        compute='_get_doctor_from_sale_order',
        readonly=True,
        store=True
    )
    patient = fields.Char(
        string='Paciente',
        compute='_get_patient_from_sale_order',
        readonly=True,
        store=True
    )
    hospital = fields.Char(
        string='Hospital',
        compute='_get_hospital_from_sale_order',
        readonly=True,
        store=True
    )
    num_sale_order = fields.Char(
        string='Num. Orden',
        compute='_get_num_order_from_sale_order',
        readonly=True,
        store=True
    )

    @api.depends('invoice_origin')
    def _get_doctor_from_sale_order(self):
        for inv in self:
            invoice_origin = inv.invoice_origin
            if invoice_origin and inv.move_type == 'out_invoice':
                obj_sale_order = self.env['sale.order'].search([('name','=',invoice_origin)])[0]
                inv.doctor = obj_sale_order.doctor.name
            else:
                inv.doctor = False

    @api.depends('invoice_origin')
    def _get_patient_from_sale_order(self):
        for inv in self:
            invoice_origin = inv.invoice_origin
            if invoice_origin and inv.move_type == 'out_invoice':
                obj_sale_order = self.env['sale.order'].search([('name','=',invoice_origin)])[0]
                inv.patient = obj_sale_order.patient.name
            else:
                inv.patient = False

    @api.depends('invoice_origin')
    def _get_hospital_from_sale_order(self):
        for inv in self:
            invoice_origin = inv.invoice_origin
            if invoice_origin and inv.move_type == 'out_invoice':
                obj_sale_order = self.env['sale.order'].search([('name','=',invoice_origin)])[0]
                inv.hospital = obj_sale_order.hospital_id.name
            else:
                inv.hospital = False

    @api.depends('invoice_origin')
    def _get_num_order_from_sale_order(self):
        for inv in self:
            invoice_origin = inv.invoice_origin
            if invoice_origin and inv.move_type == 'out_invoice':
                inv.num_sale_order = inv.invoice_origin
            else:
                inv.num_sale_order = False

    def all_fields(self):
        obj_accoun_move = self.env['account.move'].search([('move_type','=','out_invoice')])
        for obj in obj_accoun_move:
            obj._get_doctor_from_sale_order()
            obj._get_patient_from_sale_order()
            obj._get_hospital_from_sale_order()
            obj._get_num_order_from_sale_order()

class InheritAccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    grouped_line = fields.Boolean(default=False, copy=False)
