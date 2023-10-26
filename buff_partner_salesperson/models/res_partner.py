# -*- coding: utf-8 -*-
# © <2017> <builtforfifty>

from odoo import models, fields

class res_partner(models.Model):
	_inherit = 'res.partner'

	def _get_current_uid(self):
		return self.env.uid

	user_id = fields.Many2one(default=_get_current_uid)
        #a_company = fields.Char(
	#	string='Empresa', )	
	a_area = fields.Char(
		string='Area / Sección', )

	vr_contact = fields.Char(
		string='Nombre de contacto', )

	vr_phone_cont = fields.Char(
		string='Tel. de Contacto', )
