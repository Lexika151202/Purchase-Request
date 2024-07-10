# -*- coding: utf-8 -*-
{
    'name': "Purchase Request",

    'summary': 'This is Purchase Request summary from manifest',

    'description': 'This is Purchase Request description from manifest',

    'author': "My Company",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'hr', 'product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_request_line_views.xml',
        'views/purchase_request_views.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
