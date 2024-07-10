from datetime import date
from odoo import models, fields, api
from odoo.exceptions import UserError


class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = 'purchase_request.purchase_request'

    request_id = fields.Many2one('purchase.request', string='Request ID')
    product_id = fields.Many2one('product.template', string='Product ID')
    uom_id = fields.Many2one('uom.uom', string='Unit of measure ID')
    quantity = fields.Float(string='Quantity')
    quantity_approved = fields.Float(string='Approved Quantity')
    total = fields.Float(string='Total', compute='_compute_total')

    @api.depends('quantity', 'product_id.list_price')
    def _compute_total(self):
        for record in self:
            record.total = record.quantity * record.product_id.list_price

    @api.model
    def write(self, values):
        if self.request_id.state == 'wait':
            return super(PurchaseRequestLine, self).write(values)
        raise UserError('Approved Quantity can only be modified when the request state is "wait".')
