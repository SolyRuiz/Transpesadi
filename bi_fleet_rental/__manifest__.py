# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "Complete Rental Solution for Fleet Rental and Machine Rental",
    "version" : "15.0.0.1",
    "category" : "Rental",
    'summary': 'Car rental product rental service rent product rent car rent machine rental vehicle rental Equipment Rental fleet rental car rental machine rental real estate rental service Equipment rental property rental subscription Machinery rental recurring service',
    "description": """ 
        fleet rental app,
        odoo fleet rental
    This module use for Rental management system
Equipment Rental management
Rental agency
property rental
property lease
lease items
Odoo Rental Sale
Rental Sale
rental management system
rental orders
rental contract
rental contracts
lease contracts
car lease 
vehicle lease
product lease
leasing 
lease management
Rental Management for Product/Item/Equipment/Vehicle
Product Rental Management
Vehicle rental management
product lease management
vehicle rental management
Rental management
car rental management
lease sale
Odoo Rental Sale
Rental Sale
rental management system
Equipment hire agency
hire agency
fleet rental management
Tenant Management
Property Lease/Tenant Management
Property Lease Management
hire equipements

    """,
    "author": "BrowseInfo",
    "website" : "https://www.browseinfo.in",
    "price": 60,
    "currency": 'EUR',
    'depends' : ['base', 'mail', 'fleet', 'browseinfo_rental_management'],
    "data": [
        'security/ir.model.access.csv',
        'security/fleet_security.xml',
        'views/fleet_rent_views.xml',
        'views/fleet_delivery_vehicle.xml'
    ],
    "auto_install": False,
    "installable": True,
    "live_test_url":'https://youtu.be/FeoNwEeBeY8',
    "images":["static/description/Banner.png"],
    'license': 'OPL-1',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
