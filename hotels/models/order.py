import datetime
from dateutil import tz
from odoo import fields, models, api
from . sysdef import ARRIVAL_TIME_LIST


class Order(models.Model):
    _name = 'hotels.order'
    _description = 'Order'

    name = fields.Char('Number', required=True)
    order_date = fields.Date('Order date')
    guest_id = fields.Many2one('res.partner', domain="[('hotels_partner_type', '=', 'type_guest')]")
    arrival_date = fields.Datetime('Arrival date')
    departure_date = fields.Date('Departure date')
    hotel_id = fields.Many2one('hotels.hotel', string='Hotel')
    arrival_time = fields.Selection(string='Arrival Time', selection=ARRIVAL_TIME_LIST)
    invoice_id = fields.Many2one('hotels.invoice', string='Invoice', required=True,
                                 domain="[('hotel_id', '=', hotel_id)]")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

    @api.onchange('guest_id')
    def _onchange_guest(self):
        self.guest_id.hotels_partner_type = 'type_guest'

    @api.onchange('hotel_id')
    def _onchange_hotel(self):
        self.invoice_id = False
        if self.hotel_id:
            self.arrival_time = self.hotel_id.arrival_time_std

    @api.onchange('invoice_id')
    def _onchange_invoice(self):
        self.update({'hotel_id': self.invoice_id.hotel_id.id})

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

    @api.onchange('arrival_time')
    def _onchange_arrival_time(self):
        if self.arrival_date:
            dst_tz_name = self.env.user.tz
            new_date = datetime.datetime(year=self.arrival_date.year, month=self.arrival_date.month,
                                         day=self.arrival_date.day, hour=int(self.arrival_time), minute=0)
            new_date = new_date.astimezone(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            self.update({'arrival_date': new_date})

