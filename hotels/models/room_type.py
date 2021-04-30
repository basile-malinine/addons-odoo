from odoo import fields, models


class RoomType(models.Model):
    _name = 'hotels.room_type'
    _description = 'Room Type'

    name = fields.Char(string='Room type')
    hotel_id = fields.Many2one('hotels.hotel', string='Hotel')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    price = fields.Monetary('Price')

    hz_id = fields.Integer()
    hz_hotel_id = fields.Integer()
    hz_last_update = fields.Datetime()
