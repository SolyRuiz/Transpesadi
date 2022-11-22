# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import date, time, datetime
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT


class SaleOrder(models.Model):
	_inherit = 'sale.order'
	
	diagnose_id = fields.Many2one('fleet.diagnose', string='Car Diagnosis', readonly=True)
	fleet_repair_id  = fields.Many2one('fleet.repair',string='Car Repair')
	workorder_id =  fields.Many2one('fleet.workorder', string='Repair Work Order', readonly=True)
	is_workorder_created = fields.Boolean(string = "Workorder Created")
	count_fleet_repair  = fields.Integer(string='Repair Orders', compute='_compute_repair_id')
	workorder_count = fields.Integer(string='Work Orders', compute='_compute_workorder_id')

	@api.depends('fleet_repair_id')
	def _compute_repair_id(self):
		for order in self:
			repair_order_ids = self.env['fleet.repair'].search([('sale_order_id', '=', order.id)])            
			order.count_fleet_repair = len(repair_order_ids)

	@api.depends('is_workorder_created')
	def _compute_workorder_id(self):
		for order in self:
			work_order_ids = self.env['fleet.workorder'].search([('sale_order_id', '=', order.id)])            
			order.workorder_count = len(work_order_ids)

	def workorder_created(self):
		self.write({'state':'workorder'})

	def action_confirm(self):
		order  = self
		order.state = 'sale'
		fleet_line_obj = self.env['fleet.repair.line']
		if  order.diagnose_id:
			wo_vals = {
					'name': order.diagnose_id.name,
					'client_id': order.diagnose_id.client_id.id,
					'sale_order_id': order.id,
					'fleet_repair_id': order.diagnose_id.fleet_repair_id.id,
					'diagnose_id': order.diagnose_id.id,
					'hour': sum((line.est_ser_hour for line in order.diagnose_id.fleet_repair_line), 0.0),
					'priority': order.diagnose_id.priority,
					'state': 'draft',
					'user_id': order.diagnose_id.user_id.id,
					'confirm_sale_order' : True,
				}
			wo_id = self.env['fleet.workorder'].create(wo_vals)
			for line in order.diagnose_id.fleet_repair_line:
					fleet_line_vals = {
						'workorder_id': wo_id,
					}
					line.write({'workorder_id':wo_id.id})
					fleet_line_obj.write({'fleet_repair_line': line.id})
			diag_id = order.diagnose_id.id
			diagnose_obj = self.env['fleet.diagnose'].browse(diag_id)
			diagnose_obj.is_workorder_created = True
			diagnose_obj.confirm_sale_order = True
			if diagnose_obj.fleet_repair_id:
				repair_id = [diagnose_obj.fleet_repair_id.id]
				browse_record = self.env['fleet.repair'].browse(repair_id)
				browse_record.state= 'saleorder'
				browse_record.workorder_id = wo_id.id
				browse_record.confirm_sale_order = True
			self.write({'workorder_id': wo_id.id, 'fleet_repair_id':diagnose_obj.fleet_repair_id.id, 'is_workorder_created':True})
		res = super(SaleOrder, self).action_confirm()
		return res

	def button_view_repair(self):
		list = []
		context = dict(self._context or {})
		repair_order_ids = self.env['fleet.repair'].search([('sale_order_id', '=', self.id)])         
		for order in repair_order_ids:
			list.append(order.id)
		return {
			'name': _('Fleet Repair'),
			'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'fleet.repair',
			'view_id': False,
			'type': 'ir.actions.act_window',
			'domain': [('id', 'in',list )],
			'context': context,
		}

	def button_view_workorder(self):
		list = []
		context = dict(self._context or {})
		work_order_ids = self.env['fleet.workorder'].search([('sale_order_id', '=', self.id)])           
		for order in work_order_ids:
			list.append(order.id)
		return {
			'name': _('Fleet Work Order'),
			'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'fleet.workorder',
			'view_id': False,
			'type': 'ir.actions.act_window',
			'domain': [('id', 'in',list )],
			'context': context,
		}

	# TO CREATE WORKORDER ON SHIP CREATE ###

	def action_view_work_order(self):
		mod_obj = self.env['ir.model.data']
		act_obj = self.env['ir.actions.act_window']
		work_order_id = self.workorder_id.id
		result = mod_obj._xmlid_lookup("%s.%s" % ('car_repair_industry', 'action_fleet_workorder_tree_view'))[1:3]
		id = result and result[1] or False
		result = act_obj.browse(id).read()[0]
		res = mod_obj._xmlid_lookup("%s.%s" % ('car_repair_industry', 'view_fleet_workorder_form'))[1:3]
		result['views'] = [(res and res[1] or False, 'form')]
		result['res_id'] = work_order_id or False
		return result


class SaleAdvancePaymentInv(models.TransientModel):
	_inherit = "sale.advance.payment.inv"
	_description = "Sales Advance Payment Invoice"

	def create_invoices(self):
		res = super(SaleAdvancePaymentInv, self).create_invoices()
		if self._context.get('active_id'):
			sale_obj = self.env['sale.order'].browse(self._context.get('active_id'))
			if sale_obj.diagnose_id and sale_obj.diagnose_id.fleet_repair_id:
				sale_obj.diagnose_id.fleet_repair_id.write({'state': 'invoiced'})
		return res


class AccountInvoice(models.Model):
	_inherit = "account.move"
	
	create_form_fleet = fields.Boolean(string='Fleet')
	
	@api.model
	def create(self, vals):
		if vals.get('invoice_origin'):
			sale_obj = self.env['sale.order'].search([('name', '=', vals.get('invoice_origin'))])
			if sale_obj  and sale_obj.workorder_id and sale_obj.workorder_id.fleet_repair_id:
				vals.update({'create_form_fleet': True})
		return super(AccountInvoice, self).create(vals)

	def write(self,vals):
		if vals.get('state'):
			if vals.get('state') == 'posted':
				for move in self:
					sale_obj = self.env['sale.order'].search([('name', '=', move.invoice_origin)])
					if sale_obj  and sale_obj.workorder_id and sale_obj.workorder_id.fleet_repair_id:
						repair_obj = self.env['fleet.repair'].search([('id', '=', sale_obj.workorder_id.fleet_repair_id.id)])
						repair_obj.write({'state': 'done'})
		return super(AccountInvoice, self).write(vals)


class MailComposeMessage(models.TransientModel):
	_inherit = 'mail.compose.message'

	def send_mail(self, auto_commit=False):
		if self._context.get('default_model') == 'sale.order' and self._context.get('default_res_id') and self._context.get('mark_so_as_sent'):
			order = self.env['sale.order'].browse([self._context['default_res_id']])
			if order.state == 'draft':
				order.state = 'sent'
				if order.diagnose_id and order.diagnose_id.fleet_repair_id:
					order.diagnose_id.fleet_repair_id.write({'state': 'quote'})
			self = self.with_context(mail_post_autofollow=True)
		return super(MailComposeMessage, self).send_mail(auto_commit=auto_commit)


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'
	
	license_plate = fields.Char(string="License Plate")
	car_model = fields.Char(string="Model #")   

	def _prepare_invoice_line(self, **optional_values):
		"""
		Prepare the dict of values to create the new invoice line for a sales order line.

		:param qty: float quantity to invoice
		"""
		self.ensure_one()
		res = {
			'license_plate' : self.license_plate,
			'car_model' : self.car_model,
			'display_type': self.display_type,
			'sequence': self.sequence,
			'name': self.name,
			'product_id': self.product_id.id,
			'product_uom_id': self.product_uom.id,
			'quantity': self.qty_to_invoice,
			'discount': self.discount,
			'price_unit': self.price_unit,
			'tax_ids': [(6, 0, self.tax_id.ids)],
			'analytic_account_id': self.order_id.analytic_account_id.id,
			'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
			'sale_line_ids': [(4, self.id)],
		}
		if self.display_type:
			res['account_id'] = False
		return res


class AccountInvoiceLine(models.Model):
	_inherit = 'account.move.line'
	
	license_plate = fields.Char(string="License Plate")
	car_model = fields.Char(string="Model #")                   
