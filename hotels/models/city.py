from odoo import fields, models


class City(models.Model):
    _name = 'hotels.city'
    _description = 'City'

    name = fields.Char('City', index=True)

    hz_id = fields.Integer()
