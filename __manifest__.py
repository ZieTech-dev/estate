# -*- coding: utf-8 -*-
{
    'name': "estate",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
    Module de gestion immobilière
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    
    'depends': ['base', 'mail'],
    'external_dependencies': {'python': ['python-dateutil']},

    
    'data': [
        'security/ir.model.access.csv',  
        'data/estate_intervention_sequence.xml',  
        'data/estate_location_sequence.xml',      
        'views/commodite_views.xml',
        'views/etat_des_lieux_views.xml',
        'views/intervention_views.xml',
        'views/location_views.xml',
        'views/partner_views.xml',
        'views/piece_views.xml',
        'views/propriete_views.xml',
        'views/type_piece_views.xml',
        'views/type_propriete_views.xml',
        'views/estate_menu.xml',
    ],
   
    
    'application': True,
}

