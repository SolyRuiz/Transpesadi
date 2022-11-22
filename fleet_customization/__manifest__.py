# -*- coding: utf-8 -*-


{
    'name': "Fleet Customization",
    'version': "15.0.0.0",
    'category': "Invoicing",
    'summary': "Fleet Customization.",
    'description': """Fleet Customization.""",
    'author': "",
    "website": "",
    "price": 00.00,
    'currency': "EUR",
    'depends': ['base', 'sale', 'fleet', 'sale_renting', 'hr', 'car_repair_industry', 'bi_fleet_rental'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/rental_orders_views.xml',
    ],
    'license':'OPL-1',
    'installable': True,
    'auto_install': False,
    'application': False,
    "live_test_url": '',
    "images":[""],
}
