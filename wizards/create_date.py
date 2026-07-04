from odoo import api, fields, models

class CreateDate(models.TransientModel):
    _name = "create.date"
    _description = "delivery date wizard"

    end_date = fields.Date(string="delivery date")

    def action_done(self):
        self.ensure_one()
        self.write({'state': 'done','end_date':fields.Date.today()})
        self.env['vechicle.service'].create({'end_date': self.end_date})
        return {
            'type': 'ir.actions.act_window_close',

        }

    def action_create_date(self):
        self.env['vechicle.service'].create({'end_date':self.end_date})
        return {
            'type': 'ir.actions.act_window_close',

        }