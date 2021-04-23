from odoo import fields, models

HOTELS_PARTNER_TYPE_LIST = [
    ('type_hotelier', 'Hotelier'),
    ('type_guest', 'Guest'),
]


class Partner(models.Model):
    _inherit = 'res.partner'
    hotels_partner_type = fields.Selection(string='Partner type', selection=HOTELS_PARTNER_TYPE_LIST)


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'
    hotel_id = fields.Many2one('hotels.hotel', 'Hotel', ondelete='cascade', index=True)
