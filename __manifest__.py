# -*- coding: utf-8 -*-
{
    'name': "Modulo de aprendizaje",

    'summary': """Aprendiendo a utilzar Odoo""",

    'description': """
      
    """,

    'author': "Quadit",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tutorial',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account'],

    # always loaded
    'data': [
       'views/academy.xml',
       'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        
    ],
}