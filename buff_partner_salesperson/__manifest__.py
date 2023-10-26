# -*- coding: utf-8 -*-
# © <2017> <builtforfifty>
###############################################################################
#
#    Copyright (C) 2017-TODAY builtforfifty(<https://www.builtforfifty.com/odoo>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
{
    'name': "Partner Salesperson",
    'summary': "Automatically add creator as salesperson when creating partners",
    'version': '0.0.1',
    'category': 'Extra Tools',
    'website': 'https://builtforfifty.com/odoo',
    'author': 'Abu Uzayr @ builtforfifty',
    'application': False,
    'installable': True,
    'depends': [
        'base',
        'iap_crm',
        'crm',
    ],
    'data': [
        'views/partner_views.xml',
    ],
    'images': [
        'static/description/buff_partner_salesperson_banner.png',
    ],
    'test': [
    ],
}
