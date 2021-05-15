from odoo import fields, models

HOTELS_PARTNER_TYPE_LIST = [
    ('type_hotelier', 'Hotelier'),
    ('type_guest', 'Guest'),
]


class Partner(models.Model):
    _inherit = 'res.partner'
    is_hotelier = fields.Boolean(string='Is Hotelier', invisible='1')
    is_guest = fields.Boolean(string='Is Guest')

    hz_id = fields.Integer()
    hz_last_update = fields.Datetime()


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'
    hotel_id = fields.Many2one('hotels.hotel', 'Hotel', ondelete='cascade', index=True)
