from odoo import api, fields, models

_selection = [
    ('1', 'FACTURA MAL EMITIDA'),
    ('2', 'NOTA DE CREDITO-DEBITO MAL EMITIDA'),
    ('3', 'DATOS DE EMISION INCORRECTOS'),
    ('4', 'FACTURA O NOTA DE CREDITO-DEBITO DEVUELTA'),
]


class AccountMoveReversal(models.TransientModel):
    _inherit = "account.move.reversal"

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        res['vr_estado'] = self.get_vr_estado()
        return res

    vr_codigo_motivo = fields.Selection(
        _selection,
        string='Motivo de Anulación',
    )

    vr_estado = fields.Selection([
        ('send', 'Enviado'),
        ('cancelled', 'Anulado'),
    ],
        string='Estado SIAT',
    )

    def get_vr_estado(self):
        obj_move = self.env['account.move'].browse(self.env.context.get('active_id'))
        if obj_move:
            return obj_move.vr_estado
        else:
            return False

    @api.onchange('vr_codigo_motivo')
    def onchange_vr_codigo_motivo(self):
        for res in self:
            if res.vr_codigo_motivo:
                value = list(filter(lambda x: res.vr_codigo_motivo in x, _selection))[0][1]
                res.reason = value

    def reverse_moves(self):
        obj_move = self.env['account.move'].browse(self.env.context.get('active_id'))
        if obj_move and obj_move.move_type == 'out_invoice':
            if obj_move.vr_codigo_recepcion and obj_move.vr_estado == 'send':
                obj_move.vr_codigo_motivo=self.vr_codigo_motivo
                self.env['vr.operations'].cancel_invoice(obj_inv=obj_move)
                obj_move.vr_estado = 'cancelled'
        res = super(AccountMoveReversal, self).reverse_moves()
        return res