from odoo import fields, models, api
import datetime
import requests
from . import hotel
from . import contract
from . import city


class HotelsImport(models.TransientModel):
    _name = 'hotels.import_hz'
    _description = 'Hotels Import HZ'

    def get_city_id(self, name_city):
        city_id = self.env['hotels.city'].search([('name', '=', name_city)], limit=1).id
        if city_id:
            return city_id
        else:
            return self.env['hotels.city'].create({'name': name_city}).id

    def get_hotelier_id(self, name_hotelier):
        hotelier_id = self.env['res.partner'].search([('name', '=', name_hotelier)]).id
        if hotelier_id:
            return hotelier_id
        else:
            rec = self.env['res.partner'].create({'name': name_hotelier})
            rec.update({'hotels_partner_type': 'type_hotelier', 'company_type': 'person'})
            return rec.id

    def new_contract(self, hotel_id):
        return self.env['hotels.contract'].create({'name': 'NO NUMBER', 'hotel_id': hotel_id})

    def import_test(self, param):
        new_hotel_fields = {}
        for model_name in param.keys():
            if model_name == 'hotel':
                for fld_name in param['hotel']:
                    if fld_name == 'city':
                        city_id = self.get_city_id(param['hotel']['city'])
                        new_hotel_fields.update({'city_id': city_id})
                    elif fld_name == 'hotelier':
                        hotelier_id = self.get_hotelier_id(param['hotel']['hotelier'])
                        new_hotel_fields.update({'hotelier_id': hotelier_id})
                    else:
                        new_hotel_fields.update({fld_name: param['hotel'][fld_name]})
        hotel_rec = self.env['hotels.hotel'].create(new_hotel_fields)
        contract_rec = self.new_contract(hotel_rec.id)
        hotel_rec.update({'contracts_ids': [0, contract_rec.id], 'hz_last_update': datetime.datetime.now()})
        return 'hz_last_update: ' + hotel_rec.hz_last_update.strftime('%Y-%m-%d %H:%M:%S') + '   ' + \
               'id: ' + str(hotel_rec.id) + '   hz_id: ' + str(hotel_rec.hz_id)

