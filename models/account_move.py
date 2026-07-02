from odoo import fields,models,api

class ResPartner(models.Model):
    _inherit = 'account.move'

    service_id = fields.Many2one('vechicle.service', string="service")
