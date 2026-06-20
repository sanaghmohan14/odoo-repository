from odoo import fields, models

class VehicleTag(models.Model):
    _name = 'vehicle.tag'
    _description = 'Vehicle Tag'

    name = fields.Char('Tag Name', required=True, translate=True)
    color = fields.Integer('Color')
