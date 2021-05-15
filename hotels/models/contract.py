from odoo import fields, models, api


class Contract(models.Model):
    _name = 'hotels.contract'
    _description = 'Contract'

    name = fields.Char(string='Number')
    contract_date = fields.Date(string='Date')
    hotel_id = fields.Many2one('hotels.hotel', string='Hotel', required=True)
    commission = fields.Float('Commission %')
    invoices_ids = fields.One2many('hotels.invoice', 'contract_id', string='Invoices')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    attachment = fields.Binary()

    @api.onchange('hotel_id')
    def _onchange_hotel(self):
        self.commission = self.hotel_id.commission
