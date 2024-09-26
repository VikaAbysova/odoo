# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Estate',
    'version': '1.0',
    'license': 'LGPL-3',
    'author': 'Btech',
    'category': 'Real Estate',
    'sequence': 15,
    'summary': '',
    'description': "Real estate module",
    'website': '',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'demo': [
    ],
    'css': [''],
}
