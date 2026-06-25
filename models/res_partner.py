from odoo import fields,models,api

class ResPartner(models.Model):
    _inherit = 'res.partner'


    service_historys = fields.Char(string="service history", action="action_service_history_1")
    partner_id = fields.Many2one('res.partner', string="customer", required=True)
    repairs_count = fields.Integer(string="repairs_count", compute='repair_count_employee')

    def action_service_history_1(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'service_historys',
            'res_model': 'res.partner',
            'domain': [('partner_id', '=', self.id)],
            'view_mode': 'list,form',
            'view_type': 'form',

        }

    """this function is used to show the list form of service history for a customer in customer form"""


    def repair_count_employee(self):
        for rec in self:
            rec.repairs_count = self.env['vechicle.service'].search_count([('partner_id','=',self.id)])

        """this is used to count the number of repair done by the customer"""