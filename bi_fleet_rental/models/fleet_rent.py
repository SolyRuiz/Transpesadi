# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import base64
import datetime
from odoo import models, fields, api, _


class FleetVehicleInherit(models.Model):
    _inherit = 'fleet.vehicle'

    product_id = fields.Many2one('product.product', string="Product", domain=[('rent_ok', '=' ,True)])
    rent_per_month = fields.Float(string="Rent per Month", default=0.00, related="product_id.rent_per_month", store=True)
    rent_per_week = fields.Float(string="Rent per Week", default=0.00, related="product_id.rent_per_week", store=True)
    rent_per_day = fields.Float(string="Rent per Day", default=0.00, related="product_id.rent_per_day", store=True)

    _sql_constraints = [
        ('fleet_product_uniq', 'unique (product_id)', 'Product must be unique per Fleet.')
    ]
  
    @api.model
    def create(self, vals):
        res = super(FleetVehicleInherit, self).create(vals)
        if 'product_id' in vals:
            product_record = self.env['product.product'].browse(vals.get('product_id'))
            license_plate = ''
            if res.license_plate:
                license_plate = res.license_plate
            product_record.write({'fleet_id' : res.id,'license_plate' : license_plate})
        return res

    def write(self, vals):
        if 'license_plate' in vals:
            license_plate = vals.get('license_plate') or ''
            self.product_id.write({'license_plate' : license_plate})
        if 'product_id' in vals:
            product_record = self.env['product.product'].browse(vals.get('product_id'))
            license_plate = self.license_plate or ''
            if 'license_plate' in vals:
                license_plate = vals.get('license_plate') or ''
            self.product_id.write({'fleet_id' : False,'license_plate' : ''})
            product_record.write({'fleet_id' : self.id, 'license_plate' : license_plate})
        return super(FleetVehicleInherit, self).write(vals)


class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    fleet_id = fields.Many2one('fleet.vehicle', string="Fleet")
    license_plate = fields.Char(string='License Plate')
    rent_per_week = fields.Float(string="Rent per Week", default=0.00)
    rent_per_day = fields.Float(string="Rent per Day", default=0.00)



class RantalOrderLineInherit(models.Model):
    _inherit = 'sale.rental.order.line'

    fleet_id = fields.Many2one('fleet.vehicle', string="Fleet", related="product_id.fleet_id", store=True)
    license_plate = fields.Char(string='License Plate', related="product_id.license_plate", store=True)


class RantalOrderLineInherit(models.Model):
    _inherit = 'rental.order.line'

    fleet_id = fields.Many2one('fleet.vehicle', string="Fleet", related="product_id.fleet_id", store=True)
    license_plate = fields.Char(string='License Plate', related="product_id.license_plate", store=True)