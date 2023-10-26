from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    vr_server = fields.Char(
        string='Servidor Versatil',
        help='Servidor Principal Versatil',
        config_parameter="vr_server",
    )