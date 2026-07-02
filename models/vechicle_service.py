
from odoo import fields,models,api
from odoo.orm.decorators import ondelete


class VechicleService(models.Model):
    _name="vechicle.service"
    _description = "vechicle service"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one('res.partner',string="customer",required=True)
    mobile_number = fields.Char(related='partner_id.phone',)
    email = fields.Char(related='partner_id.email',string="Email")
    advisor_id = fields.Many2one('res.users',string="advisor",required=True)
    vechicle_no = fields.Char(string="vechicle no",copy=False,required=True)
    state = fields.Selection([('draft','draft'),('inprogress','inprogress'),('ready','ready'),('cancelled','cancelled'),('done','done')],string="state",required=True,tracking=True,default="draft")
    vechicle_image = fields.Image(string="vechicle image",max_width=1920,max_height=1920)
    vechicle_type = fields.Many2one('fleet.vehicle.model.category',string="category",ondelete="set null")
    vehicle_model = fields.Many2one('fleet.vehicle.model',string="vehicle model")
    service_type = fields.Selection([('option1','free'),('option2','paid')],string="service type",required=True)
    start_date = fields.Date(string="start date",default=fields.Date.today())
    duration = fields.Integer(string="duration")
    end_date = fields.Date(string="delivery date")
    estimated_amount = fields.Float(string="estimated amount")
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
    invoice_count = fields.Integer(string="invoices",compute="no_of_invoice")
    invoice_paid = fields.Selection([('paid','paid'),('unpaid','unpaid')],compute='compute_invoice_paid',widget="ribbon")
    active = fields.Boolean(string="Active",default=True)
    invoice_id = fields.Many2one('account.move')
    sub_total_amount = fields.Float(string="sub total amount", compute='employee_cost')
    hourly_cost = fields.Float(string="hourly cost of employee")
    hours_spent = fields.Float(string="hours spent")
    service_id = fields.Many2one('vechicle.service',string="service")



    def action_confirm(self):
        """the action confirmm is used to
                 change the state to in progress when clicked the confrim button"""
        self.state='inprogress'



    def action_ready_for_delivery(self):
        self.state='ready'

    def action_done(self):
        self.state='done'





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
        print("hi")




    def action_invoice(self):
        self.ensure_one()
        print("hey")
        """the action invoice is used to create an invoice"""


        invoice = self.env['account.move'].create({'move_type': 'out_invoice', 'partner_id': self.partner_id.id,'service_id': self.id})

        labor_cost = self.env.ref('vechicle_repair_management.labor_cost_product')

        description="labor cost \n"

        labor_sum = sum(self.labor_working_details_ids.mapped('sub_total_amount'))
        for i in self.labor_working_details_ids:

            description+=f"{i.labor_name.name} {i.hours_spent} hours"
        self.env['account.move.line'].create(
                {
                    'move_id': invoice.id,
                    'product_id': labor_cost.id,
                    'quantity': 1,
                    'price_unit': labor_sum,
                    'name':description,
                    # 'name': f"labor-{i.labor_name.name}  ,{i.hours_spent} Hours , {i.employee_assigned_to_labor.name} manager"

                }
            )

        for line in self.consumed_parts_ids:
            self.env['account.move.line'].create(
                {
                    'move_id': invoice.id,
                    'product_id': line.product_id.id,
                    'quantity': line.quantity,
                    'price_unit': line.unit_price,
                    'name': line.product_id.name,

                }
            )

        self.invoice_id = invoice.id







    def action_view_invoice(self):
        self.ensure_one()
        """this function is used to view the generated invoice when clicking the button"""
        invoice=self.env['account.move'].search([('move_type','=', 'out_invoice'), ('partner_id','=',self.partner_id.id)])
        if len(invoice)==1:

            return{
            'type': 'ir.actions.act_window',
            'name': 'invoice_id',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'view_type': 'form',
            'quantity':1,
            'domain':[('service_id','=',self.id)],
            'view_mode':'form',
            'target':'current'
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'invoice_id',
                'res_model': 'account.move',
                'res_id': self.invoice_id.id,
                'view_type': 'list,form',
                'quantity': 1,
                'domain': [('service_id','=',self.id),],
                'view_mode': 'list,form'
            }



    def no_of_invoice(self):
        """repair count function is used to calculate the number of repair services done by the customer"""
        for rec in self:
            rec.invoice_count=self.env['account.move'].search_count([('partner_id','=',rec.partner_id.id)])



    def compute_invoice_paid(self):
        """this is to show the count of invoice in smart button"""
        for rec in self:
            if rec.invoice_id and rec.invoice_id.payment_state == 'paid':
                rec.invoice_paid='paid'
            else:
                rec.invoice_paid='unpaid'

    @api.depends('hourly_cost', 'hours_spent')
    def employee_cost(self):
        """employee cost is used to calculate the wage of the employee based on the hourly cost and hours spent by the employee on the work"""
        for rec in self:
            # rec.sub_total_amount = rec.hourly_cost * rec.hours_spent if rec.hourly_cost else rec.hours_spent
            rec.sub_total_amount = rec.hourly_cost * rec.hours_spent

    def action_send_mail(self):
        template=self.env.ref('vechicle_repair_management.vehicle_service_template')
        for rec in self:
            if template:
                # 3. Send the email
                template.send_mail(rec.id, force_send=True)
            else:
                print("no template")















