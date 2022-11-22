# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import UserError


class FleetRepairChecklist(models.Model):
    _name = 'fleet.repair.checklist'
    _description = "FLEET REPAIR Checklist"

    name = fields.Char('Checklist Name', required=True, translate=True)
    active = fields.Boolean(default=True)

    def unlink(self):
        fleet_repair_obj = self.env['fleet.repair']
        rule_ranges = fleet_repair_obj.search([('repair_checklist_ids', 'in', self.ids)])
        if rule_ranges:
            raise UserError(
                _("You Are Trying To Delete a Record That Is Still Referenced!\nInstead Delete The Record Use Archive"))
        return super(FleetRepairChecklist, self).unlink()
