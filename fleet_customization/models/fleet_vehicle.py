# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class VehicleTags(models.Model):
    _inherit = 'fleet.vehicle.tag'

    tag_type = fields.Selection([('Chasis','Chasis'),('Cabezal','Cabezal')], string="Tag Type", 
        default='Cabezal', required=True)


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if self._context.get('Cabezal'):
            find_tag_ids = self.env['fleet.vehicle.tag'].search([('tag_type','=','Cabezal')])
            args = [('tag_ids','in',find_tag_ids.ids),('state_id.sequence','=',4)]
 
        if self._context.get('Chasis'):
            find_tag_ids = self.env['fleet.vehicle.tag'].search([('tag_type','=','Chasis')])
            args = [('tag_ids','in',find_tag_ids.ids),('state_id.sequence','=',4)]

        if self._context.get('Cabezal_Chasis'):
            find_tag_ids = self.env['fleet.vehicle.tag'].search([('tag_type','in',['Chasis', 'Cabezal'])])
            end_result = self._context.get('end_result')
            document_type = self._context.get('document_type')
            if end_result == 'Disponible' and document_type == 'Entregar':
                sequence = 8
            else:
                sequence = 7
            args = [('tag_ids','in',find_tag_ids.ids),('state_id.sequence','=',sequence)]
        

        return super()._name_search(name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

    
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        args = args or []
        if self._context.get('Cabezal'):
            find_tag_ids = self.env['fleet.vehicle.tag'].search([('tag_type','=','Cabezal')])
            args = [('tag_ids','in',find_tag_ids.ids),('state_id.sequence','=',4)]
 
        if self._context.get('Chasis'):
            find_tag_ids = self.env['fleet.vehicle.tag'].search([('tag_type','=','Chasis')])
            args = [('tag_ids','in',find_tag_ids.ids),('state_id.sequence','=',4)]

        if self._context.get('Cabezal_Chasis'):
            find_tag_ids = self.env['fleet.vehicle.tag'].search([('tag_type','in',['Chasis', 'Cabezal'])])
            end_result = self._context.get('end_result')
            document_type = self._context.get('document_type')
            if end_result == 'Disponible' and document_type == 'Entregar':
                sequence = 8
            else:
                sequence = 7
            args = [('tag_ids','in',find_tag_ids.ids),('state_id.sequence','=',sequence)]

        return super().search(args, offset=0, limit=None, order=None, count=False)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if self._context.get('Cabezal'):
            find_tag_ids = self.env['fleet.vehicle.tag'].search([('tag_type','=','Cabezal')])
            vehicle_ids = self.env['fleet.vehicle'].search([('tag_ids','in',find_tag_ids.ids)])
            partner_ids = vehicle_ids.mapped('driver_id')
            args = [('id','in',partner_ids.ids)]
        
        if self._context.get('Chasis'):
            find_tag_ids = self.env['fleet.vehicle.tag'].search([('tag_type','=','Chasis')])
            vehicle_ids = self.env['fleet.vehicle'].search([('tag_ids','in',find_tag_ids.ids)])
            partner_ids = vehicle_ids.mapped('driver_id')
            args = [('id','in',partner_ids.ids)]

        return super()._name_search(name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        args = args or []
        if self._context.get('Cabezal'):
            find_tag_ids = self.env['fleet.vehicle.tag'].search([('tag_type','=','Cabezal')])
            vehicle_ids = self.env['fleet.vehicle'].search([('tag_ids','in',find_tag_ids.ids)])
            partner_ids = vehicle_ids.mapped('driver_id')
            args = [('id','in',partner_ids.ids)]
        
        if self._context.get('Chasis'):
            find_tag_ids = self.env['fleet.vehicle.tag'].search([('tag_type','=','Chasis')])
            vehicle_ids = self.env['fleet.vehicle'].search([('tag_ids','in',find_tag_ids.ids)])
            partner_ids = vehicle_ids.mapped('driver_id')
            args = [('id','in',partner_ids.ids)]

        return super().search(args, offset=0, limit=None, order=None, count=False)

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if self._context.get('is_mechanic'):
            employee_ids = self.env['hr.employee'].search([('job_id.is_mechanic','=',True)])
            args = [('id','in',employee_ids.mapped('user_id').ids)]

        return super()._name_search(name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)
    
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        args = args or []
        if self._context.get('is_mechanic'):
            employee_ids = self.env['hr.employee'].search([('job_id.is_mechanic','=',True)])
            args = [('id','in',employee_ids.mapped('user_id').ids)]

        return super().search(args, offset=0, limit=None, order=None, count=False)