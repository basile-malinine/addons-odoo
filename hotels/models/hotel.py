from odoo import fields, models, api
from . sysdef import *


class Hotel(models.Model):
    _name = 'hotels.hotel'
    _description = 'Hotel'

    name = fields.Char(string='Name', required=True)
    num_stars = fields.Selection(string='Stars', selection=NUM_STARS_LIST, default='a')
    # region_id
    city_id = fields.Many2one('hotels.city', string='City')
    address = fields.Char('Address')
    phone = fields.Char('Phone')
    email = fields.Char('E-Mail')
    hotelier_id = fields.Many2one('res.partner', string='Hotelier',
                                  domain="[('hotels_partner_type', '=', 'type_hotelier')]")
    fine_period = fields.Selection(selection=FINE_PERIOD_LIST)
    fine_size = fields.Selection(selection=FINE_SIZE_LIST)
    banks_ids = fields.One2many('res.partner.bank', 'hotel_id', string='Bank Accounts')
    contacts_ids = fields.Many2many('res.partner', string='Contacts')
    room_types_ids = fields.One2many('hotels.room_type', 'hotel_id', string='Rooms')
    contracts_ids = fields.One2many('hotels.contract', 'hotel_id', string='Contracts')
    invoices_ids = fields.One2many('hotels.invoice', 'hotel_id', string='Invoices')
    commission = fields.Float(default=0.12)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    arrival_time_std = fields.Selection(selection=ARRIVAL_TIME_LIST, string='Arrival time (standard)', default='14')

    hz_id = fields.Integer()
    hz_last_update = fields.Datetime()

    @api.onchange('hotelier_id')
    def _onchange_hotelier(self):
        self.hotelier_id.hotels_partner_type = 'type_hotelier'
