#-*- coding:utf-8 -*-
{
    'name': "RP Form Hide Archive, Delete and Duplicate Option",
    'version': '13.0.1.0.0',
    'description': "Hide archive, delete and duplicate options in form view",
    'summary': 'This module helps to show archive, delete and duplicate options from form view based on groups.',
    'author': 'RP Odoo Developer ',
    'category': 'Web',
    'license': "OPL-1",
    'depends': ['web'],
    'data': [
        'security/groups.xml',
        'views/assets.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
}
