from odoo import api, fields, models
import requests


class Company(models.Model):
    _inherit = 'res.company'

    url_hz = fields.Char(default='http://frichono.ru')
    num_hotels_in_paket = fields.Integer(default=100)


class HotelsSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    url_hz = fields.Char(default=lambda self: self.env.user.company_id.url_hz)
    num_hotels_in_paket = fields.Integer(default=lambda self: self.env.user.company_id.num_hotels_in_paket)

    @api.onchange('url_hz')
    def _onchange_url_hz(self):
        self.env.user.company_id.url_hz = self.url_hz

    def test_url(self):
        resp = requests.post(self.url_hz)
        print(resp)

    @api.onchange('num_hotels_in_paket')
    def _onchange_hotels_in_paket(self):
        self.env.user.company_id.num_hotels_in_paket = self.num_hotels_in_paket

    def import_hotels(self):
        resp = requests.post(self.url_hz + '/oda/action',
                             data={'entity': 'hotels', 'num': self.num_hotels_in_paket, 'exp': 1, 'pass': 123456789})
        print(resp)
