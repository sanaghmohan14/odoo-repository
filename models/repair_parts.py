from odoo import fields,models,api
class RepairParts(models.Model):
    _name='repair.parts'

    consumed_parts_id = fields.Many2one('vechicle.service')
    product_id = fields.Many2one('product.product',domain=[('type',"!=",['service'])])
    quantity = fields.Float(string="QTY")
    unit_price = fields.Float(related='product_id.list_price')
    sub_total_price = fields.Float(string="TOTAL" ,compute='total_price')
    consumed_parts_ids = fields.One2many('repair.parts', 'consumed_parts_id')


    @api.depends('quantity','unit_price')
    def total_price(self):
        for record in self:
                # record.sub_total_price = record.unit_price * record.quantity if record.quantity else record.unit_price
                record.sub_total_price = record.unit_price * record.quantity

    """total price is used to find the tota price of a product based on the quantity of the product"""




