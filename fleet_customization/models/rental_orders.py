# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class RentalOrderLine(models.Model):
    _inherit = 'sale.order.line'

    cabezal_id = fields.Many2one('fleet.vehicle', string="Cabezal")
    chasis_id = fields.Many2one('fleet.vehicle', string="Chasis")
    piloto_id = fields.Many2one('res.partner', string="Piloto")


class RentalOrder(models.Model):
    _inherit = 'sale.order'

    cabezal_id = fields.Many2one('fleet.vehicle', string="Cabezal")
    chasis_id = fields.Many2one('fleet.vehicle', string="Chasis")
    piloto_id = fields.Many2one('res.partner', string="Piloto")

    @api.onchange('cabezal_id')
    def _onchange_sale_cabezal(self):
        for sale in self:
            if not sale.cabezal_id:
                sale.piloto_id = False

            if sale.cabezal_id:
                sale.piloto_id = sale.cabezal_id.driver_id and sale.cabezal_id.driver_id.id

    def action_confirm(self):
        res = super(RentalOrder, self).action_confirm()
        for so in self:
            if so.cabezal_id:
                state_id = self.env['fleet.vehicle.state'].search([('sequence','=',5)])
                if state_id:
                    so.cabezal_id.write({
                        'state_id' : state_id and state_id.id
                    })

            if so.chasis_id:
                state_id = self.env['fleet.vehicle.state'].search([('sequence','=',5)])
                if state_id:
                    so.chasis_id.write({
                        'state_id' : state_id and state_id.id
                    })

    def _create_invoices(self, grouped=False, final=False, date=None):
        """Link timesheets to the created invoices. Date interval is injected in the
        context in sale_make_invoice_advance_inv wizard.
        """
        moves = super()._create_invoices(grouped=grouped, final=final, date=date)
        for so in self:
            if so.cabezal_id:
                state_id = self.env['fleet.vehicle.state'].search([('sequence','=',6)])
                if state_id:
                    so.cabezal_id.write({
                        'state_id' : state_id and state_id.id
                    })

            if so.chasis_id:
                state_id = self.env['fleet.vehicle.state'].search([('sequence','=',6)])
                if state_id:
                    so.chasis_id.write({
                        'state_id' : state_id and state_id.id
                    })
        return moves

    def _prepare_invoice(self):
        invoice_vals = super(RentalOrder, self)._prepare_invoice()
        invoice_vals['cabezal_id'] = self.cabezal_id and self.cabezal_id.id or False
        invoice_vals['chasis_id'] = self.chasis_id and self.chasis_id.id or False
        invoice_vals['piloto_id'] = self.piloto_id and self.piloto_id.id or False
        return invoice_vals


class AccountMove(models.Model):
    _inherit = 'account.move'

    cabezal_id = fields.Many2one('fleet.vehicle', string="Cabezal")
    chasis_id = fields.Many2one('fleet.vehicle', string="Chasis")
    piloto_id = fields.Many2one('res.partner', string="Piloto")

    def action_post(self):
        res = super(AccountMove, self).action_post()
        for so in self:
            if so.cabezal_id:
                state_id = self.env['fleet.vehicle.state'].search([('sequence','=',7)])
                if state_id:
                    so.cabezal_id.write({
                        'state_id' : state_id and state_id.id
                    })

            if so.chasis_id:
                state_id = self.env['fleet.vehicle.state'].search([('sequence','=',7)])
                if state_id:
                    so.chasis_id.write({
                        'state_id' : state_id and state_id.id
                    })
        return res


class HRJob(models.Model):
    _inherit = 'hr.job'

    is_mechanic = fields.Boolean('Is Mechanic')


class RecieveDeliverVehicle(models.Model):
    _inherit = 'receive.deliver.vehicle'

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")

    def write(self, vals):
        res = super(RecieveDeliverVehicle, self).write(vals)
        if vals.get('end_result'):
            state_id = self.env['fleet.vehicle.state']
            if self.end_result == 'Disponible':
                state_id = self.env['fleet.vehicle.state'].search([('sequence','=',4)])
            if self.end_result == 'Taller':
                state_id = self.env['fleet.vehicle.state'].search([('sequence','=',8)])
            if state_id:
                self.vehicle_id.write({
                    'state_id' : state_id and state_id.id
                })
        return res
    
    @api.model
    def create(self, vals):
        res = super(RecieveDeliverVehicle, self).create(vals)
        if vals.get('end_result'):
            state_id = self.env['fleet.vehicle.state']
            if res.end_result == 'Disponible':
                state_id = self.env['fleet.vehicle.state'].search([('sequence','=',4)])
            if res.end_result == 'Taller':
                state_id = self.env['fleet.vehicle.state'].search([('sequence','=',8)])
            if state_id:
                res.vehicle_id.write({
                    'state_id' : state_id and state_id.id
                })
        return res