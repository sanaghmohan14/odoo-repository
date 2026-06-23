from email.policy import default

from PIL.ImageChops import duplicate
from isodate import duration
from openpyxl.worksheet import related

from odoo import fields,models,api
from odoo . fields import Domain
from odoo import fields, models,api

class VechicleService(models.Model):
    _name="vechicle.service"
    _description = "vechicle service"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id=fields.Many2one('res.partner',string="customer",required=True)
    mobile_number=fields.Char(related='partner_id.phone',required=True,)
    advisor_id=fields.Many2one('res.users',string="advisor",required=True)
    vechicle_no=fields.Char(string="vechicle no",copy=False)
    state=fields.Selection([('draft','draft'),('inprogress','inprogress'),('ready','ready for delivery'),('cancelled','cancelled')],string="state",required=True,tracking=True,default="draft")
    vechicle_image=fields.Image(string="vechicle image",max_width=1920,max_height=1920)
    vechicle_type=fields.Many2one('fleet.vehicle.model.category',string="category",required=True)
    vehicle_model=fields.Many2one('fleet.vehicle.model',string="vehicle model")
    service_type=fields.Selection([('option1','free'),('option2','paid')],string="service type",required=True)
    start_date=fields.Date(string="start date",required=True,default=fields.Date.today())
    duration=fields.Integer(string="duration",required=True)
    end_date=fields.Date(string="delivery date")
    estimated_amount=fields.Float(string="estimated amount",required=True)
    customer_compliant=fields.Text(string="customer complaint")
    tag_ids = fields.Many2many('vehicle.tag', string="tags")
    company_id=fields.Many2one('res.company',string="Company",default=lambda self: self.env.company,readonly=True)
    name = fields.Char(string='', readonly=True ,default='New')
    service_tag=fields.Many2many('service.tag',string="service tags")


    # labor

    labor_name=fields.Many2one('res.partner',string="Labor")
    employee_assigned_to_labor=fields.Many2one('res.users',string="manager of labor")
    # working_schedule=fields.Many2one('resource.calender')

    hourly_cost=fields.Float(string="hourly cost of employee")
    hours_spent=fields.Float(string="hours spent")
    sub_total_amount=fields.Float(string="sub total amount",compute='employee_cost')

   #consumed parts

    product_id=fields.Many2one('product.product',string="consumed parts")
    quantity=fields.Float(string="quantity")
    unit_price=fields.Float(related='product_id.list_price')
    sub_total_price=fields.Float(string="sub total price" ,compute='total_price')
    service_history=fields.Char(string="service history")


    def action_confirm(self):
        self.state='inprogress'

    @api.model
    def create(self,vals_list):
        for vals in vals_list:
            if vals.get('name','New')=='New':
                vals['name']=self.env['ir.sequence'].next_by_code('vehicle.reference') or 'New'
            return super().create(vals_list)

    #service history form

    def action_service_history(self):
        return {
            'type': 'ir.actions.act_window',
            'name':'service_history',
            'res_model':'vechicle.service',
            'domain':[('partner_id','=',self.partner_id.id)],
            'view_mode':'list,form',
            'view_type': 'form',

        }


    @api.depends('quantity','unit_price')
    def total_price(self):
        for record in self:
                record.sub_total_price = record.unit_price * record.quantity if record.quantity else record.unit_price


    @api.depends('hourly_cost','hours_spent')
    def employee_cost(self):
        for i in self:
            i.sub_total_amount=i.hourly_cost*i.hours_spent if i.hourly_cost else i.hours_spent




















































