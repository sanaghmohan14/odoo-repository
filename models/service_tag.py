from odoo import fields,models

class ServiceTag(models.Model):
    _name = 'service.tag'
    _description = 'Service Tag'

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color')
