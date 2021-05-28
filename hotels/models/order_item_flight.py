import datetime
from dateutil import tz
from odoo import fields, models, api
from .sysdef import *


# Позиция в Заказе: Авиа билеты (Flight)
class OrderItemFlight(models.Model):
    _name = 'hotels.order.item.flight'
    _description = 'Flight'

    name = fields.Char(string='Title')
    order_id = fields.Many2one(comodel_name='hotels.order', string='Order')
    quantity = fields.Float(string='Quantity')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    price = fields.Monetary(string='Price')
    price_total = fields.Monetary(string='Total')

    # Если при импорте код валюты не найден,
    # здесь сохраняется оригинальный код из Hotelzov
    hz_currency_code = fields.Char()
    hz_id = fields.Integer()
    hz_last_update = fields.Datetime()

