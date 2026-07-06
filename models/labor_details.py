from odoo import fields,models,api
class LaborDetails(models.Model):
    _name = 'labor.details'

    labor_details_id = fields.Many2one('vechicle.service')
    labor_name_id = fields.Many2one('res.partner',string="Labor")
    employee_assigned_to_labor_id = fields.Many2one('res.users',string="manager of labor")
    hourly_cost = fields.Float(string="hourly cost of employee")
    hours_spent = fields.Float(string="hours spent")
    sub_total_amount = fields.Float(string="sub total amount",compute='employee_cost')
    labor_working_details_ids = fields.One2many('labor.details', 'labor_details_id')
    labor_total_amount = fields.Float(string="total amount")

    # labor_cost_product=fields.Many2one('product.product',string="labor product")


    @api.depends('hourly_cost','hours_spent')
    def employee_cost(self):
        """employee cost is used to calculate the wage of the employee based on the hourly cost and hours spent by the employee on the work"""
        for rec in self:
            # rec.sub_total_amount=rec.hourly_cost*rec.hours_spent if rec.hourly_cost else rec.hours_spent
            rec.sub_total_amount = rec.hourly_cost * rec.hours_spent






