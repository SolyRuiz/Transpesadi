# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import base64
import datetime
from odoo import models, fields, api, _


class IrRule(models.Model):
    _inherit = 'ir.rule'

    @api.model
    def disable_fleet_company_rule(self):
        rol_id = self.env.ref('fleet.ir_rule_fleet_vehicle')
        rol_id.write({'active':False})

    @api.model
    def disable_product_company_rule(self):
        rol_id = self.env.ref('product.product_comp_rule')
        rol_id.write({'active':False})


class FleetVehicleInherit(models.Model):
    _inherit = 'fleet.vehicle'

    product_id = fields.Many2one('product.product', string="Product", domain=[('rent_ok', '=' ,True)])
    rent_per_month = fields.Float(string="Rent per Month", default=0.00, related="product_id.rent_per_month", store=True)
    rent_per_week = fields.Float(string="Rent per Week", default=0.00, related="product_id.rent_per_week", store=True)
    rent_per_day = fields.Float(string="Rent per Day", default=0.00, related="product_id.rent_per_day", store=True)
    company_ids = fields.Many2many('res.company', string='Company')

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
    _inherit = 'product.template'

    company_ids = fields.Many2many('res.company', string='Company')


class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    fleet_id = fields.Many2one('fleet.vehicle', string="Fleet")
    license_plate = fields.Char(string='License Plate')
    rent_per_week = fields.Float(string="Rent per Week", default=0.00)
    rent_per_day = fields.Float(string="Rent per Day", default=0.00)
    company_ids = fields.Many2many('res.company', string='Company')


class RantalOrderLineInherit(models.Model):
    _inherit = 'sale.rental.order.line'

    fleet_id = fields.Many2one('fleet.vehicle', string="Fleet", related="product_id.fleet_id", store=True)
    license_plate = fields.Char(string='License Plate', related="product_id.license_plate", store=True)


class RantalOrderLineInherit(models.Model):
    _inherit = 'rental.order.line'

    fleet_id = fields.Many2one('fleet.vehicle', string="Fleet", related="product_id.fleet_id", store=True)
    license_plate = fields.Char(string='License Plate', related="product_id.license_plate", store=True)


class RentalOrder(models.Model):
    _inherit = 'rental.order'

    contact_rental_ids = fields.One2many('fleet.vehicle.log.contract', 'contract_id', string='Rental Contracts')


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    end_result = fields.Selection([('Disponible','Disponible'),('Taller','Taller')], string="Ingresar resultados")

class FleetVehicleLogContract(models.Model):
    _inherit = 'fleet.vehicle.log.contract'

    cliente = fields.Char('Cliente')
    partner_id = fields.Many2one('res.partner', string='Cliente')
    ubicacion_de_alquiler = fields.Char(string='Ubicación de alquiler')
    terminos_iniciales = fields.Char(string='Términos iniciales')
    frecuencia_de_facturacion = fields.Char(string='Frecuencia de facturación')
    fecha_de_orden = fields.Date(string='Fecha de orden')
    almacen = fields.Char(string='Almacén')
    contract_id = fields.Many2one('rental.order', string="Rental Order")
    picking_ids = fields.Many2many('stock.picking', compute='_compute_picking_ids', string='Picking associated to this Rental')
    delivery_count = fields.Integer(string='Recibir y entregar vehículo', compute='_compute_picking_ids')
    rd_vehicle_id = fields.Many2one('receive.deliver.vehicle', 'Recibir y entregar vehículo')
    end_result = fields.Selection([('Disponible','Disponible'),('Taller','Taller')], string="Ingresar resultados")

    def _compute_picking_ids(self):
        pickings = []
        for order in self:
            order.delivery_count = self.env['receive.deliver.vehicle'].search_count([('contract_log_id','=',self.id)])

    def action_view_delivery_rental(self):
        '''
        This function returns an action that display existing delivery orders
        of given sales order ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        '''
        
        result = {
            'name': 'Recibir y entregar vehículo',
            'type': 'ir.actions.act_window',
            'binding_view_types': 'list,form',
            'view_mode': 'tree,form',
            'res_model': 'receive.deliver.vehicle',
        }
        if not self.rd_vehicle_id:
            vals = {
                'document_type' : 'Recibir',
                'deadline_date' : self.expiration_date,
                'partner_id' : self.partner_id.id,
                'client' : self.cliente,
                'last_odoomtr' : '',
                'received_by' : '',
                'deliver_by' : '',
                'phone' : self.partner_id.phone,
                'contract_id' : self.contract_id and self.contract_id.id,
                'contract_log_id' : self.id
            }

            rd_vehicle_id = self.env['receive.deliver.vehicle'].create(vals)

            self.write({
                'rd_vehicle_id' : rd_vehicle_id.id
            })

        domain = [('contract_log_id','=',self.id)]

        # form = self.env.ref('bi_fleet_rental.receive_deliver_vehicle_form', False)
        # form_id = form.id if form else False
        # result['views'] = [(form_id, 'form')]
        # result['res_id'] = self.rd_vehicle_id and self.rd_vehicle_id.id
        result['domain'] = domain
        return result


class ChecklistEntries(models.Model):
    _name = 'checklist.entry'

    name = fields.Char(string='Checklist')
    user_id = fields.Many2one('res.users', string="Assigned by", default=lambda self: self.env.user.id, track_visibility='always')


class ChecklistLines(models.Model):
    _name = 'checklist.lines'
    _description = 'checklist'
    _rec_name = 'checklist_id'

    checklist_id = fields.Many2one('checklist.entry')
    user_id = fields.Many2one('res.users', string="Assigned by")
    rd_vehicle_id = fields.Many2one('receive.deliver.vehicle', 'Recibir y entregar vehículo')

    @api.onchange('checklist_id')
    def _onchange_checklist(self):
        if self.checklist_id:
            self.user_id = self.checklist_id.user_id and self.checklist_id.user_id.id or self.env.user.id


class ReceiveDeliverVehicle(models.Model):
    _name = 'receive.deliver.vehicle'
    _description = 'Recibir y entregar vehículo'
    _rec_name = 'contract_id'

    document_type = fields.Selection([('Recibir','Recibir'),('Entregar','Entregar')], 
        string='Tipo documento', default='Recibir', required=True)
    deadline_date = fields.Date('Fecha de entrega')
    partner_id = fields.Many2one('res.partner', 'Cliente')
    client = fields.Char('Cliente')
    last_odoomtr = fields.Char('Último odómetro')
    odoomtr_id = fields.Many2one('fleet.vehicle.odometer', string="Odoo Meter")
    received_by = fields.Char('Recibido por')
    deliver_by = fields.Char('Entregado por')
    phone = fields.Char('Teléfono')
    check_list_ids = fields.One2many('checklist.lines', 'rd_vehicle_id', 'Checklist')   
    contract_id = fields.Many2one('rental.order', string="Rental Order")
    contract_log_id = fields.Many2one('fleet.vehicle.log.contract', string="Contract")
    end_result = fields.Many2one('fleet.vehicle.state', string="Ingresar resultados")

    def write(self, vals):
        res = super(ReceiveDeliverVehicle, self).write(vals)
        if vals.get('end_result',False):
            self.contract_log_id.vehicle_id.write({
                'state_id' : self.end_result.id
            })
        return res

# class FleetVehicleState(models.Model):
#     _inherit = 'fleet.vehicle.state'

#     is_ingresar_resultados = fields.Boolean('Is Ingresar resultados ?')