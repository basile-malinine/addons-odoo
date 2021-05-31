from odoo import fields, models


class PriceOption(models.Model):
    _name = 'hotels.price_option'
    _description = 'Price Option'

    label = fields.Char(string='Price option')
    room_type_id = fields.Many2one('hotels.room_type', string='Room type')
    quantity = fields.Float(string='Quantity')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    price = fields.Monetary(string='Price')

    hz_id = fields.Integer()
