from odoo import fields,models,api

class AccountMove(models.Model):
    _inherit = 'account.move'

    service_id = fields.Many2one('vechicle.service', string="Service")
