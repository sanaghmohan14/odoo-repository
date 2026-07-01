from odoo import api, fields, models

class CreateVechicleService(models.TransientModel):
    _name = "create.vechicle.service"
    _description = "Vechicle Service wizard"

    partner_id = fields.Many2one('res.partner', string="customer", required=True)
    vechicle_no = fields.Char(string="vechicle no", copy=False, required=True)
    mobile_number = fields.Char(related='partner_id.phone', required=True, )
    advisor_id = fields.Many2one('res.users', string="advisor", required=True)
    service_type = fields.Selection([('option1', 'free'), ('option2', 'paid')], string="service type", required=True)


    def action_create_service(self):

        self.env['vechicle.service'].create({'partner_id':self.partner_id.id,
                                             'advisor_id':self.advisor_id.id,
                                             'vechicle_no':self.vechicle_no,
                                             'service_type':self.service_type,})
        return {
            'type':'ir.actions.act_window_close',




        }