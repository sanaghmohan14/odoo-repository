from odoo import fields,models,api
class LaborDetails(models.Model):
    _name='labor.details'

    labor_details_id=fields.Many2one('vechicle.service')

    labor_name=fields.Many2one('res.partner',string="Labor")
    employee_assigned_to_labor=fields.Many2one('res.users',string="manager of labor")
    hourly_cost=fields.Float(string="hourly cost of employee")
    hours_spent=fields.Float(string="hours spent")
    sub_total_amount=fields.Float(string="sub total amount",compute='employee_cost')
    total_one=fields.Float(string="total amount")


    @api.depends('hourly_cost','hours_spent')
    def employee_cost(self):
        for i in self:
            i.sub_total_amount=i.hourly_cost*i.hours_spent if i.hourly_cost else i.hours_spent


