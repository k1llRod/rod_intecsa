# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import random

from odoo import api, fields, models, _
from odoo.exceptions import AccessDenied, AccessError, UserError
from odoo.tools import html_escape

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.onchange('partner_id')  # if these fields are changed, call method
    def _check_change(self):
        self.user_id = self.partner_id.user_id