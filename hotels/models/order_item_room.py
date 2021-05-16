import datetime
from dateutil import tz
from odoo import fields, models, api
from .sysdef import *


# Позиция в Заказе: Размещение (Accommodation)
class OrderItemRoom(models.Model):
    _name = 'hotels.order.item.room'
    _description = 'Accommodation'

    order_id = fields.Many2one(comodel_name='hotels.order', string='Order')
    hotel_id = fields.Many2one(comodel_name='hotels.hotel', string='Hotel')
    room_type_id = fields.Many2one(comodel_name='hotels.room_type',
                                   domain="[('hotel_id', '=', hotel_id)]", string='Room')
    arrival_date = fields.Date(string='Arrival date')
    departure_date = fields.Date(string='Departure date')
    quantity = fields.Integer(string='Quantity')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    price = fields.Monetary(string='Price')
    price_total = fields.Monetary(string='Total')

    @api.onchange('hotel_id')
    def _onchange_hotel_id(self):
        self.room_type_id = False

    @api.onchange('room_type_id')
    def _onchange_room_type_id(self):
        if self.room_type_id:
            self.price = self.room_type_id.price
            self.currency_id = self.room_type_id.currency_id
