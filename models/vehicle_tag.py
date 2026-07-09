from odoo import fields,models

class VehicleTag(models.Model):
    _name = 'vehicle.tag'
    _description = 'Vehicle Tag'
    _check_company_auto = True

    name = fields.Char('Tag Name', required=True, translate=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company, readonly=True)
    color = fields.Integer('Color')
