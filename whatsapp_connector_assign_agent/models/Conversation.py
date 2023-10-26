# -*- coding: utf-8 -*-
import logging
from odoo import models, api
from odoo.addons.whatsapp_connector.tools import date_timedelta
_logger = logging.getLogger(__name__)


class Conversation(models.Model):
    _inherit = 'acrux.chat.conversation'

    def get_to_done(self):
        out = super(Conversation, self).get_to_done()
        if not out.get('agent_id'):
            out['agent_id'] = self.agent_id.id
        return out

    def get_to_new(self):
        out = super(Conversation, self).get_to_new()
        if not out.get('agent_id') and not self.env.context.get('ignore_assign_agent'):
            out['agent_id'] = self.get_default_agent()
        return out

    def get_possible_agents(self):
        self.ensure_one()
        agent_ids = self.env['res.users']
        connector_id = self.connector_id
        if connector_id.assing_type == 'connector':
            agent_ids = connector_id.agent_ids
        elif connector_id.assing_type == 'crm_team':
            team_id = self.team_id or connector_id.team_id
            agent_ids = team_id.member_ids
        agent_ids = agent_ids.filtered(lambda x: self.user_exist_and_active_or_offline(x))
        if self.agent_id and self.env.context.get('ignore_agent_id'):
            agent_ids -= self.agent_id
        return agent_ids

    def get_default_agent(self):
        self.ensure_one()
        agent_id = False
        auto_assign = self.connector_id.automatic_agent_assign
        agent_ids = self.get_possible_agents() if auto_assign else []
        commercial_id = self.res_partner_id.user_id
        if not self.env.context.get('ignore_agent_id'):
            # Verifica que agente está en la lista solo si activado 'asignación automática'
            if self.connector_id.assign_commercial and commercial_id and \
                    self.user_exist_and_active_or_offline(commercial_id) and \
                    (not auto_assign or (auto_assign and commercial_id in agent_ids)):
                agent_id = commercial_id.id
            elif self.connector_id.retain_agent and self.agent_id and \
                    self.user_exist_and_active_or_offline(self.agent_id) and \
                    (not auto_assign or (auto_assign and self.agent_id in agent_ids)):
                agent_id = self.agent_id.id
        if not agent_id and auto_assign and agent_ids:
            userindex = self.env['acrux.chat.user.index']
            agent_id = userindex.assign_index(self.connector_id.id, agent_ids)
        return agent_id

    def user_exist_and_active_or_offline(self, user_id):
        return bool(user_id and (self.connector_id.assign_offline_agent or user_id.chatroom_active()))

    @api.model
    def conversation_verify_reassign_agent_search(self, conn_id):
        if conn_id.time_to_reasign:
            date_to_news = date_timedelta(minutes=-conn_id.time_to_reasign)
            return self.search([('connector_id', '=', conn_id.id),
                                ('status', '=', 'new'),
                                ('last_received_first', '!=', False),
                                ('last_received_first', '<', date_to_news)])
        else:
            return self.env['acrux.chat.conversation']

    @api.model
    def conversation_verify_reassign_agent(self):
        ''' Call from cron or direct '''
        Connector = self.env['acrux.chat.connector'].sudo()
        to_news_ids = 0
        for conn_id in Connector.search([('automatic_agent_assign', '=', True)]):
            sctx = self.sudo().with_context(tz=conn_id.tz,
                                            lang=conn_id.company_id.partner_id.lang,
                                            allowed_company_ids=[conn_id.company_id.id])
            to_news = sctx.conversation_verify_reassign_agent_search(conn_id)
            if len(to_news):
                to_news_ids += len(to_news)
                for to_x in to_news:
                    to_x.event_create('unanswered', user_id=to_x.agent_id)
                    agent_id = to_x.with_context(ignore_agent_id=True).get_default_agent()
                    to_x.agent_id = agent_id.id
                    to_x.tmp_agent_id = False
                    to_x.delegate_conversation()
        _logger.info('________ | conversation assign_agent: %s' % to_news_ids)
