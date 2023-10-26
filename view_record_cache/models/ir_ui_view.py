# -*- coding: utf-8 -*-

import hashlib

from odoo import models, fields, api, tools, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError, ValidationError, UserError
import logging

_logCache = logging.getLogger(__name__+'_Cache')
_logger = logging.getLogger(__name__)

PREFETCH_MAX=models.PREFETCH_MAX

class View(models.Model):
    _inherit='ir.ui.view'
    
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False,_cache={}):
        groups_id=self.env.user.groups_id.ids
        lang=self.env.context.get('lang')
        key="%s%s%s%s%s%s%s%s" % (str(self.ids),
                                str(offset),
                                str(args),
                                str(lang or 'lang'),
                                str(limit or 'limit'),
                                str(order or 'order'),
                                str(count or 'count'),
                                str(groups_id))  
        hashKey = hashlib.sha1(key.encode('utf-8') or '').hexdigest()
        key_hash=str(hashKey)
        if not key_hash in _cache:
            result = super(View, self).search(args, offset=offset, limit=limit, order=order, count=count)
            _cache[key_hash]=result
        result= _cache[key_hash]
        return result if count else self.browse(result.ids)
    
    
    
    # @api.multi
    def read(self, fields=None, load='_classic_read',_cache={}):
        """ call the method get_empty_list_help of the model and set the window action help message
        """
        groups_id=self.env.user.groups_id.ids
        lang=self.env.context.get('lang')
        key='%s%s%s%s%s'%(str(self.ids),
                          str(fields or 'fields'),
                          str(load),
                          str(groups_id),
                          str(lang or 'lang')
                                        ) 
        key_hash=str(hashlib.sha1(key.encode('utf-8') or '').hexdigest())
        if not key_hash in _cache or self.env.context.get('install_mode'):
            result = super(View, self).read(fields, load=load)
            _cache[key_hash]=result
        result=_cache[key_hash]
        for vals in result:
            record = self.browse(vals['id'])
        return result
    
    
        
