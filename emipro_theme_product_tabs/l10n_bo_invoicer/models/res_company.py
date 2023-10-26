from odoo import fields, models, _
from odoo.exceptions import AccessError


class ResCompany(models.Model):
    _inherit = "res.company"

    vr_api_key = fields.Char(
        string='API KEY',
        help='Código de autorización',
        config_parameter="vr_api_key",
    )

    def check_connection_with_versatil(self):
        response = self.env['vr.operations'].check_connection_siat()
        if response and response['connection']:
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': ('Conexión exitosa!. Cliente: ' + response['client']),
                    'type': 'rainbow_man',
                }
            }
        else:
            raise AccessError(_('No se pudo establecer conexión con Versatil. Verifique que sean correctos los siguientes parámetros:\n- El "Servidor Versatil" en configuraciones generales.\n- El código "API KEY" en esta pantalla.'))