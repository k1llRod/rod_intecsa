# -*- coding: utf-8 -*-
from odoo import api, exceptions, fields, models, _
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.constrains('active')
    def check_product_active(self):
        if self.env.user.has_group('pw_restrict_archive.group_archive_product'):
            raise UserError(_('You have no access to archive/unarchive product !'))
