import datetime
from dateutil import tz
from odoo import fields, models, api
from . sysdef import *


class Order(models.Model):
    _name = 'hotels.order'
    _description = 'Order'

    name = fields.Char('Number', required=True)
    hotel_id = fields.Many2one('hotels.hotel', string='Hotel')
    guest_id = fields.Many2one('res.partner', domain="[('is_guest', '=', True)]")
    room_type_id = fields.Many2one('hotels.room_type', domain="[('hotel_id', '=', hotel_id)]")
    order_date = fields.Date(string='Order date')
    status = fields.Selection(string='Status', selection=ORDER_STATUS_LIST)
    arrival_date = fields.Date(string='Arrival date')
    departure_date = fields.Date(string='Departure date')
    arrival_time = fields.Selection(string='Arrival Time', selection=TIME_LIST)
    invoice_id = fields.Many2one('hotels.invoice', string='Invoice',
                                 domain="[('hotel_id', '=', hotel_id)]")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    price = fields.Monetary(string='Price')

    # Если при импорте код валюты не найден,
    # здесь сохраняется оригинальный код из Hotelzov
    hz_currency_code = fields.Char()

    hz_id = fields.Integer()
    hz_last_update = fields.Datetime()

    @api.onchange('guest_id')
    def _onchange_guest(self):
        self.guest_id.is_guest = True

    @api.onchange('hotel_id')
    def _onchange_hotel(self):
        self.invoice_id = False
        if self.hotel_id:
            self.arrival_time = self.hotel_id.arrival_time_std

    # При изменении Даты заезда в Заказе
    # Время в Дате заезда в Заказе == Время заезда в заказе (+ корректировка TZ)
    @api.onchange('arrival_date')
    def _onchange_arrival_date(self):
        dst_tz_name = self.env.user.tz
        new_date = False
        if self.arrival_time and self.arrival_date:
            new_date = datetime.datetime(year=self.arrival_date.year, month=self.arrival_date.month,
                                         day=self.arrival_date.day, hour=int(self.arrival_time), minute=0,
                                         tzinfo=tz.gettz(dst_tz_name))
        elif self.arrival_date:
            new_date = datetime.datetime(year=self.arrival_date.year, month=self.arrival_date.month,
                                         day=self.arrival_date.day, hour=0, minute=0,
                                         tzinfo=tz.gettz(dst_tz_name))
        if new_date:
            new_date = new_date.astimezone(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            self.update({'arrival_date': new_date})

    # При изменении Времени заезда в Заказе
    # Время в Дате заезда в Заказе == Время заезда в заказе (+ корректировка TZ)
    @api.onchange('arrival_time')
    def _onchange_arrival_time(self):
        if self.arrival_date:
            dst_tz_name = self.env.user.tz
            new_date = datetime.datetime(year=self.arrival_date.year, month=self.arrival_date.month,
                                         day=self.arrival_date.day, hour=int(self.arrival_time), minute=0)
            new_date = new_date.astimezone(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            self.update({'arrival_date': new_date})

