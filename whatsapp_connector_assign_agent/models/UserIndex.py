# -*- coding: utf-8 -*-
from odoo import models, fields, api


class UserIndex(models.TransientModel):
    _name = 'acrux.chat.user.index'
    _description = 'Chat User Index'
    _rec_name = 'connector'
    _order = 'id desc'

    connector = fields.Integer('Connector', required=True)
    user_index = fields.Integer('User Index')

    @api.model
    def assign_index(self, connector, agent_ids):
        user_index = self.search([('connector', '=', connector)], limit=1).user_index
        user_index = user_index or 0
        size = len(agent_ids.ids)
        index = user_index % size
        user = agent_ids.ids[index]
        self.create({'connector': connector, 'user_index': index + 1})
        return user
