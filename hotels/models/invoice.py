from odoo import fields, models, api


class Invoice(models.Model):
    _name = 'hotels.invoice'
    _description = 'Invoice'

    name = fields.Char('Number')
    invoice_date = fields.Date('Date')
    hotel_id = fields.Many2one('hotels.hotel', string='Hotel', readonly=False)
    contract_id = fields.Many2one('hotels.contract', string='Contract', required=True,
                                  domain="[('hotel_id', '=', hotel_id)]")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    price_total = fields.Monetary(string='Total')

    @api.onchange('hotel_id')
    def _onchange_hotel(self):
        self.contract_id = False

    # @api.onchange('contract_id')
    # def _onchange_contract(self):
    #     self.update({'hotel_id': self.contract_id.hotel_id.id})
