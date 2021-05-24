from odoo import api, fields, models
import requests


class Company(models.Model):
    _inherit = 'res.company'

    is_test_url = fields.Boolean()
    is_url_ok = fields.Boolean()
    url_hz = fields.Char()
    num_hotels_in_paket = fields.Integer(default=100)
    num_orders_in_paket = fields.Integer(default=100)


class HotelsSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    url_hz = fields.Char(default=lambda self: self.env.user.company_id.url_hz)
    num_hotels_in_paket = fields.Integer(default=lambda self: self.env.user.company_id.num_hotels_in_paket)
    num_orders_in_paket = fields.Integer(default=lambda self: self.env.user.company_id.num_orders_in_paket)

    is_test_url = fields.Boolean(default=False)
    is_url_ok = fields.Char(default=lambda self: self.env.user.company_id.is_url_ok)

    @api.onchange('url_hz')
    def _onchange_url_hz(self):
        self.env.user.company_id.url_hz = self.url_hz
        if not self.env.user.company_id.is_test_url:
            return
        else:
            self.test_url(self.url_hz)
            self.env.user.company_id.is_test_url = False

    def test_url_press(self):
        self.env.user.company_id.is_test_url = True

    def test_url(self, url):
        try:
            resp = requests.post(url)
        except Exception:
            print('Error!')
            self.is_url_ok = False
        else:
            print(resp)
            self.is_url_ok = True

    @api.onchange('is_url_ok')
    def _onchange_is_url_ok(self):
        self.env.user.company_id.is_url_ok = self.is_url_ok

    @api.onchange('num_hotels_in_paket')
    def _onchange_hotels_in_paket(self):
        self.env.user.company_id.num_hotels_in_paket = self.num_hotels_in_paket

    @api.onchange('num_orders_in_paket')
    def _onchange_orders_in_paket(self):
        self.env.user.company_id.num_orders_in_paket = self.num_orders_in_paket

    def import_hotels(self):
        resp = requests.post(self.url_hz + '/oda/action',
                             data={'odoo_url': 'http://95.165.173.247:8069', 'odoo_db': 'hotelzov',
                                   'odoo_user': 'admin', 'odoo_pass': 'admin', 'entity': 'hotels',
                                   'num': self.num_hotels_in_paket, 'exp': 1, 'pass': 123456789})
        print(resp)

    def import_orders(self):
        resp = requests.post(self.url_hz + '/oda/action',
                             data={'odoo_url': 'http://95.165.173.247:8069', 'odoo_db': 'hotelzov',
                                   'odoo_user': 'admin', 'odoo_pass': 'admin', 'entity': 'orders',
                                   'num': self.num_orders_in_paket, 'exp': 1, 'pass': 123456789})
        print(resp)
