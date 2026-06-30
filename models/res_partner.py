from odoo import fields,models,api

class ResPartner(models.Model):
    _inherit = 'res.partner'


    service_historys = fields.Char(string="service history", action="action_service_history_1")
    partner_id = fields.Many2one('res.partner', string="customer", required=True)
    repairs_count = fields.Integer(string="repairs_count", compute='repair_count_employee')
    active = fields.Boolean(string="Active", default=True)


    def action_service_history_1(self):
        """this function is used to show the list form of service history for a customer in customer form"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'service_historys',
            'res_model': 'vechicle.service',
            'domain': [('partner_id', '=',self.id)],
            'view_mode': 'list,form',
            'view_type': 'form',
            'context':{'search_default_order':'end_date asc'}

        }

    def repair_count_employee(self):
        """this is used to count the number of repair done by the customer"""
        for rec in self:
            rec.repairs_count = self.env['vechicle.service'].search_count([('partner_id','=',self.id)])


    def new_form(self):
        print("123")



    def action_create_service(self):
        return {
            'type':'ir.actions.act_window',
            'res_model': 'vechicle.service',
            'view_mode':'form',
            'target':'current',
            'context':{'default_partner_id':self.id},
        }


    def write(self,vals):
        res=super().write(vals)

        if 'active' in vals and vals['active'] is False:
            repair=self.env['vechicle.service'].search(['partner_id','in',self.ids])
            repair.write({'active':False})
        return res







    invoice_id = fields.Many2one('account.move')

    def action_invoice(self):
        print("hello")
        """the action invoice is used to create an invoice"""
        invoice=self.env['account.move'].create({'move_type':'out_invoice','partner_id':self.id})
        self.invoice_id=invoice.id