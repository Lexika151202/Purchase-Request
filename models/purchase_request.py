# -*- coding: utf-8 -*-
from datetime import date

from odoo import models, fields, api
from odoo.exceptions import UserError


class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'purchase_request.purchase_request'

    department_id = fields.Many2one('hr.department', string='Department ID')
    request_id = fields.Many2one('res.users', string='Request ID')
    approved_id = fields.Many2one('res.users', string='Approved ID')
    date = fields.Date(string='Date', required=True, default=lambda self: date.today())
    date_approve = fields.Date(string='Approve date')
    request_line_ids = fields.One2many('purchase.request.line', 'request_id', string='Request line IDs')
    description = fields.Text(string='This is Purchase request description')
    state = fields.Selection([
        ('draft', 'Bản Nháp'),
        ('wait', 'Chờ Duyệt'),
        ('approved', 'Hoàn Thành'),
        ('cancel', 'Từ Chối')],
        default='draft',
        require=True
    )

    total_quantity = fields.Float(string='Total quantity', compute='_compute_total_quantity')
    total_amount = fields.Float(sring='Total amount', compute='_compute_total_amount')

    @api.depends('request_line_ids.quantity')
    def _compute_total_quantity(self):
        for record in self:
            record.total_quantity = sum(request.quantity for request in record.request_line_ids)

    @api.depends('request_line_ids.total')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(request.total for request in record.request_line_ids)

    def unlink(self):
        if self.state == 'draft':
            return super(PurchaseRequest, self).unlink()
        raise UserError('Only draft requests can be deleted.')

    def write(self, values):
        if self.state == 'wait':
            return super(PurchaseRequest, self).write({'quantity_approved': values['quantity_approved']})
        raise UserError('Only update quantity_approved in waiting state.')
