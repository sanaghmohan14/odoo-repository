
from odoo import fields,models,api

class VechicleService(models.Model):
    _name="vechicle.service"
    _description = "vechicle service"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one('res.partner',string="customer",required=True)
    mobile_number = fields.Char(related='partner_id.phone',required=True,)
    advisor_id = fields.Many2one('res.users',string="advisor",required=True)
    vechicle_no = fields.Char(string="vechicle no",copy=False)
    state = fields.Selection([('draft','draft'),('inprogress','inprogress'),('ready','ready'),('cancelled','cancelled')],string="state",required=True,tracking=True,default="draft")
    vechicle_image = fields.Image(string="vechicle image",max_width=1920,max_height=1920)
    vechicle_type = fields.Many2one('fleet.vehicle.model.category',string="category",required=True)
    vehicle_model = fields.Many2one('fleet.vehicle.model',string="vehicle model")
    service_type = fields.Selection([('option1','free'),('option2','paid')],string="service type",required=True)
    start_date = fields.Date(string="start date",required=True,default=fields.Date.today())
    duration = fields.Integer(string="duration")
    end_date = fields.Date(string="delivery date")
    estimated_amount = fields.Float(string="estimated amount",required=True)
    customer_compliant = fields.Text(string="customer complaint")
    tag_ids = fields.Many2many('vehicle.tag', string="tags")
    company_id = fields.Many2one('res.company',string="Company",default=lambda self: self.env.company,readonly=True)
    name = fields.Char(string='', readonly=True ,default='New')
    service_tag = fields.Many2many('service.tag',string="service tags")
    labor_working_details_ids = fields.One2many('labor.details','labor_details_id')
    employee_assigned_to_labor = fields.Many2one('res.users',string="manager of labor")
    consumed_parts_ids= fields.One2many('repair.parts','consumed_parts_id')
    service_history = fields.Char(string="service history",action="action_service_history")
    total = fields.Float(string="Total", compute='total_amount')
    labor_total_amount = fields.Float(string="Total",compute='labor_total')
    repair_count = fields.Integer(string="repair_count",compute='repair_count_employee')
    total_sum = fields.Float(string='Amount',compute="sum_of_cost")



    invoice_history=fields.Char(string="invoice",action="action_invoice_history")

    def action_confirm(self):
        """the action confirmm is used to
                 change the state to in progress when clicked the confrim button"""
        self.state='inprogress'

    def action_invoice(self):
        """the action invoice is used to create an invoice"""
        self.state='ready'

    def action_ready_for_delivery(self):
        self.state='ready'





    @api.model
    def create(self,vals_list):
        """create function is used to create the reference/ sequence id when creating a  new repair service """
        for vals in vals_list:
            if vals.get('name','New')=='New':
                vals['name']=self.env['ir.sequence'].next_by_code('vehicle.reference') or 'New'
            return super().create(vals_list)



    def action_service_history(self):
        """action service history is used to create an action for smart button
            when clicking on smart button the service history of the user need to be shown"""
        return {
            'type': 'ir.actions.act_window',
            'name':'service_history',
            'res_model':'vechicle.service',
            'domain':[('partner_id','=',self.partner_id.id)],
            'view_mode':'list,form',
            'view_type': 'form',

        }



    @api.depends('consumed_parts_ids.sub_total_price')
    def total_amount(self):
        """used to calculate the total amount of consumed parts"""
        for rec in self:
            rec.total=sum(rec.consumed_parts_ids.mapped('sub_total_price'))




    @api.depends('labor_working_details_ids.sub_total_amount')
    def labor_total(self):
        """calculate the total amount of labor charge"""
        for rec in self:
            rec.labor_total_amount=sum(rec.labor_working_details_ids.mapped('sub_total_amount'))





    def repair_count_employee(self):
        """repair count function is used to calculate the number of repair services done by the customer"""
        for rec in self:
            rec.repair_count=self.env['vechicle.service'].search_count([('partner_id','=',rec.partner_id.id)])



    @api.depends('labor_total_amount','total','estimated_amount')
    def sum_of_cost(self):
        """calculate sum of the amount labor charge + product charge"""
        for rec in self:
            rec.total_sum=rec.labor_total_amount+rec.total+rec.estimated_amount




    def action_invoice_history(self):
        print(" ")









































