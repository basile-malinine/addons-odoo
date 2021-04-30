from odoo import models
import datetime
import time


class HotelsImport(models.TransientModel):
    _name = 'hotels.import_hz'
    _description = 'Hotels Import HZ'

    # Создание пустого Контракта с привязкой к Отелю
    def new_contract(self, hotel_rec):
        contract_rec = self.env['hotels.contract'].create({'name': 'NO NUMBER', 'hotel_id': hotel_rec.id})
        hotel_rec.write({'contracts_ids': [(4, contract_rec.id, 0)]})
        print('Добавлен контракт - к Отелю: ' + hotel_rec.name)

    # Импорт объекта Отеля из Hotelzov
    def hotel_import(self, hz_model):
        hotel_rec = self.env['hotels.hotel'].search([('hz_id', '=', int(hz_model['id']))])
        if hotel_rec:
            # Если запись Отеля в odoo уже есть:
            if time.mktime(hotel_rec.hz_last_update.timetuple()) >= int(hz_model['changed']):
                # 1. Если экспорт записи в odoo был позже чем последнее обновление на Hotelzov,
                #    то обновление не требуется
                return hotel_rec
            else:
                # 2. Иначе обновляем пока только Наименование
                hotel_rec.update({'name': hz_model['name']})
                self.new_contract(hotel_rec)
                print('Обновление Отеля: ' + hotel_rec.name)
        else:
            # 3. Если Отель в odoo отсутствует, создаём запись с hz_id и Наименованием
            hotel_rec = self.env['hotels.hotel'].create({'hz_id': int(hz_model['id']), 'name':  hz_model['name']})
        # Для пуктов 2 и 3 обновление всех остальных не реляционных полей
        hotel_rec.update({
            'num_stars': hz_model['num_stars'],
            'address': hz_model['address'],
            'phone': hz_model['phone'],
            'email': hz_model['email'],
            'fine_period': hz_model['fine_period'],
            'fine_size': hz_model['fine_size'],
            'hz_arrival_time_std': hz_model['arrival_time_std'],
            'hz_departure_time_std': hz_model['departure_time_std'],
            'commission': float(hz_model['commission']) / 100,
            'hz_last_update': datetime.datetime.now(),
        })
        return hotel_rec

    def city_import(self, hz_model):
        city_rec = self.env['hotels.city'].search([('hz_id', '=', hz_model['id'])])
        if city_rec:
            city_rec.update({'name': hz_model['name']})
            print('Обновление Города: ' + city_rec.name)
        else:
            city_rec = self.env['hotels.city'].create({'hz_id': hz_model['id'], 'name':  hz_model['name']})
            print('Добавлен Город: ' + city_rec.name)
        return city_rec

    def hotelier_import(self, hz_model):
        hotelier_rec = self.env['res.partner'].search([('hz_id', '=', hz_model['id'])])
        if hotelier_rec:
            # Если запись Отельера в odoo уже есть:
            if time.mktime(hotelier_rec.hz_last_update.timetuple()) >= int(hz_model['access']):
                # 1. Если экспорт записи в odoo был позже чем последнее обновление на Hotelzov,
                #    то обновление не требуется
                return hotelier_rec
            else:
                # 2. Иначе обновляем пока только Наименование
                hotelier_rec.update({'name': hz_model['name']})
                print('Обновление Отельера: ' + hotelier_rec.name)
        else:
            # 3. Если Отельер в odoo отсутствует, создаём запись с id Hotelzov и Именем
            hotelier_rec = self.env['res.partner'].create({'hz_id': int(hz_model['id']), 'name': hz_model['name']})
            print('Добавление Отельера: ' + hotelier_rec.name)
        # Для пуктов 2 и 3 обновление всех остальных не реляционных полей
        hotelier_rec.update({
            'city': hz_model['city'],
            'street': hz_model['address'],
            'phone': hz_model['phone'],
            'email': hz_model['email'],
            'hz_last_update': datetime.datetime.now()
        })
        return hotelier_rec

    def room_type_import(self, hz_model):
        room_type_rec = self.env['hotels.room_type'].search([('hz_id', '=', hz_model['id'])])
        if room_type_rec:
            # Если запись Типа номера в odoo уже есть:
            if time.mktime(room_type_rec.hz_last_update.timetuple()) >= int(hz_model['changed']):
                # 1. Если экспорт записи в odoo был позже чем последнее обновление на Hotelzov,
                #    то обновление не требуется
                return room_type_rec
            else:
                # 2. Иначе обновляем пока только Наименование
                room_type_rec.update({'name': hz_model['name']})
                print('Обновление Типа номера: ' + room_type_rec.name)
        else:
            # 3. Если Тип номера в odoo отсутствует, создаём запись с id Hotelzov и Названием
            room_type_rec = self.env['hotels.room_type'].create({'hz_id': int(hz_model['id']),
                                                                 'name': hz_model['name']})
            print('Добавлен Тип номера: ' + room_type_rec.name)
        # Для пуктов 2 и 3 обновление всех остальных не реляционных полей
        currency_id = self.env['res.currency'].search([('name', '=', hz_model['currency_code'])]).id
        if currency_id:
            # Если id валюты найден по коду из Hotelzov (RUB, USD, ...), то обновляем
            room_type_rec.update({'currency_id': currency_id})
        room_type_rec.update({
            'price': float(hz_model['price']) / 100,
            'hz_last_update': datetime.datetime.fromtimestamp(int(hz_model['changed'])),
        })
        return room_type_rec

    def import_hz(self, param):
        hotel_rec = False
        if param:
            for model_name in param.keys():
                if model_name == 'hotel':
                    hotel_rec = self.hotel_import(param['hotel'])
                    if not hotel_rec.contracts_ids.ids:
                        # Если у Отеля нет контракта, добавляем новый Контракт без номера с привязкой к Отелю
                        self.new_contract(hotel_rec)
                elif model_name == 'city':
                    city_rec = self.city_import(param['city'])
                    if hotel_rec.city_id != city_rec:
                        hotel_rec.city_id = city_rec
                elif model_name == 'hotelier':
                    hotelier_rec = self.hotelier_import(param['hotelier'])
                    if hotel_rec.hotelier_id != hotelier_rec:
                        hotel_rec.hotelier_id = hotelier_rec
                elif model_name == 'room_types':
                    for room_type in param['room_types']:
                        room_type_rec = self.room_type_import(room_type)
                        if (bool(hotel_rec) and bool(room_type_rec)) and (room_type_rec not in hotel_rec.room_types_ids):
                            hotel_rec.write({'room_types_ids': [(4, room_type_rec.id, 0)]})
