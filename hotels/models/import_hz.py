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
        print('Добавлен Контракт к Отелю: ' + hotel_rec.name)

    # Импорт Города из Hotelzov
    def city_import(self, hz_model):
        city_rec = self.env['hotels.city'].search([('hz_id', '=', hz_model['id'])])
        if city_rec:
            city_rec.update({'name': hz_model['name']})
        else:
            city_rec = self.env['hotels.city'].create({'hz_id': hz_model['id'], 'name':  hz_model['name']})
            print('Добавлен Город: ' + city_rec.name)
        return city_rec

    # Импорт Отельера из Hotelzov
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
            # 3. Если Отельер в odoo отсутствует, создаём запись и заполняем hz_id и Имя
            hotelier_rec = self.env['res.partner'].create({'hz_id': int(hz_model['id']), 'name': hz_model['name']})
            print('Добавление Отельера: ' + hotelier_rec.name)
        # Для пуктов 2 и 3 обновление всех остальных не реляционных полей
        hotelier_rec.update({
            'is_hotelier': True,
            'city': hz_model['city'],
            'street': hz_model['address'],
            'phone': hz_model['phone'],
            'email': hz_model['email'],
            'hz_last_update': datetime.datetime.now(),
        })
        return hotelier_rec

    # Импорт Гостя из Hotelzov
    def guest_import(self, hz_model):
        guest_rec = self.env['res.partner'].search([('hz_id', '=', hz_model['id'])])
        if guest_rec:
            # Если запись Гостя в odoo уже есть:
            if time.mktime(guest_rec.hz_last_update.timetuple()) > int(hz_model['access']):
                # 1. Если экспорт записи в odoo был позже чем последнее обновление на Hotelzov,
                #    то обновление не требуется
                return guest_rec
            else:
                # 2. Иначе обновляем пока только Наименование
                guest_rec.update({'name': hz_model['name']})
                print('Обновление Гостя: ' + guest_rec.name)
        else:
            # 3. Если Гость отсутствует, создаём запись и заполняем hz_id и Имя
            guest_rec = self.env['res.partner'].create({'hz_id': int(hz_model['id']), 'name': hz_model['name']})
            print('Добавление Гостя: ' + guest_rec.name)
        # Для пуктов 2 и 3 обновление всех остальных не реляционных полей

        guest_rec.update({
            'is_guest': True,
            'city': hz_model['city'],
            'street': hz_model['address'],
            'phone': hz_model['phone'],
            'email': hz_model['email'],
            'hz_last_update': datetime.datetime.now(),
        })
        return guest_rec

    # Импорт Типа номера из Hotelzov
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
            # 3. Если Тип номера в odoo отсутствует, создаём запись и заполняем hz_id и Название
            room_type_rec = self.env['hotels.room_type'].create({'hz_id': int(hz_model['id']),
                                                                 'name': hz_model['name']})
            print('Добавлен Тип номера: ' + room_type_rec.name)
        # Для пуктов 2 и 3 обновление всех остальных не реляционных полей
        currency_id = self.env['res.currency'].search([('name', '=', hz_model['currency_code'])]).id
        if currency_id:
            # Если id валюты найден по коду из Hotelzov (RUB, USD, ...), то обновляем
            room_type_rec.update({'currency_id': currency_id})
        else:
            print('Тип номера: ' + room_type_rec.name + ' НЕ НАЙДЕН КОД ВАЛЮТЫ ИЗ HOTELZOV: ' + hz_model['currency_code'])
            # print('Код валюты устоновится по умолчанию для текущей компании! ' +
            #       self.env['user.company_id.currency_id'].name)
            # Сохраняем неизвестный код валюты в спец. поле
            room_type_rec.update({'hz_currency_code': hz_model['currency_code']})
        room_type_rec.update({
            'hz_currency_code': hz_model['currency_code'],
            'price': hz_model['price'],
            'hz_last_update': datetime.datetime.now(),
        })
        return room_type_rec

    # Импорт Отеля из Hotelzov
    def hotel_import(self, hz_model):
        hotel_rec = self.env['hotels.hotel'].search([('hz_id', '=', int(hz_model['id']))])
        if hotel_rec:
            # Если запись Отеля в odoo уже есть:
            if time.mktime(hotel_rec.hz_last_update.timetuple()) >= int(hz_model['changed']):
                # 1. Если экспорт записи в odoo был позже чем последнее обновление на Hotelzov,
                #    то обновление не требуется
                print('Обновление Отеля: ' + hotel_rec.name + ' не требуется')
                print('Дата odoo: ' + hotel_rec.hz_last_update.strftime('%Y-%m-%d %H:%M:%S'))
                print('Дата hotelzov: ' +
                      datetime.datetime.fromtimestamp(int(hz_model['changed'])).strftime('%Y-%m-%d %H:%M:%S'))
                return hotel_rec
            else:
                # 2. Иначе обновляем пока только Наименование
                hotel_rec.update({'name': hz_model['name']})
                print('Обновление Отеля: ' + hotel_rec.name)
        else:
            # 3. Если Отель в odoo отсутствует, создаём запись с hz_id и Наименованием
            hotel_rec = self.env['hotels.hotel'].create({'hz_id': int(hz_model['id']), 'name': hz_model['name']})
            print('Добавление Отеля: ' + hotel_rec.name)
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
            'commission': hz_model['commission'],
            'hz_last_update': datetime.datetime.now(),
        })

        if not hotel_rec.contracts_ids.ids:
            # Если у Отеля нет контракта, добавляем новый Контракт без номера с привязкой к Отелю
            self.new_contract(hotel_rec)
        if 'city' in hz_model:
            info_city = hz_model['city']
            # Импортируем Город
            city_rec = self.city_import(info_city)
            # Связываем с Отелем
            if hotel_rec.city_id != city_rec:
                hotel_rec.city_id = city_rec
        if 'hotelier' in hz_model:
            info_hotelier = hz_model['hotelier']
            # Импорт Отельера
            hotelier_rec = self.hotelier_import(info_hotelier)
            # Связывваем с Отелем
            if hotel_rec.hotelier_id != hotelier_rec:
                hotel_rec.hotelier_id = hotelier_rec
        if 'room_types' in hz_model:
            info_room_types = hz_model['room_types']
            # Для кажого Типа номера у Отеля
            for room_type in info_room_types:
                # Импортируем Тип номера
                room_type_rec = self.room_type_import(room_type)
                # Связываем с Отелем
                if room_type_rec not in hotel_rec.room_types_ids:
                    hotel_rec.write({'room_types_ids': [(4, room_type_rec.id, 0)]})
        if hotel_rec:
            print('    Отель: ' + hotel_rec.name + ' (Импорт завершён)')
        else:
            print('    Ошибка импорта Отеля...')
        return hotel_rec

    # ф-ции импорта позиций состава Заказа

    # Импорт позиции Размещения в Заказе
    def item_accommodation_import(self, hz_model):
        item_accommodation_rec = self.env['hotels.order.item.accommodation'].search([('hz_id', '=', hz_model['id'])])
        if item_accommodation_rec:
            # Если запись позиции Бронирования в odoo уже есть:
            if time.mktime(item_accommodation_rec.hz_last_update.timetuple()) >= int(hz_model['changed']):
                # 1. Если экспорт записи в odoo был позже чем последнее обновление на Hotelzov,
                #    то обновление не требуется
                print('Обновление бронирования в Заказе: ' + str(item_accommodation_rec.room_type_id.name) + ' не требуется')
                print('Дата odoo: ' + item_accommodation_rec.hz_last_update.strftime('%Y-%m-%d %H:%M:%S'))
                print('Дата hotelzov: ' +
                      datetime.datetime.fromtimestamp(int(hz_model['changed'])).strftime('%Y-%m-%d %H:%M:%S'))
                return item_accommodation_rec
            else:
                # 2. Иначе:
                print('Обновление бронирования в Заказе: ' + str(item_accommodation_rec.room_type_id.name))
        else:
            # 3. Если позиция Бронирования в odoo отсутствует, создаём запись и заполняем hz_id
            item_accommodation_rec = self.env['hotels.order.item.accommodation'].create({'hz_id': int(hz_model['id'])})
            print('Добавлено бронирование в Заказ, id: ' + str(hz_model['id']))
        # Для пуктов 2 и 3 обновление всех остальных полей

        # Ссылка на Отель
        if 'hotel' in hz_model:
            # Получаем инфо по Отелю
            info_hotel = hz_model['hotel']
            # Импорт Отеля
            hotel_rec = self.hotel_import(info_hotel)
            # Добавляем ссылку
            if item_accommodation_rec.hotel_id != hotel_rec:
                item_accommodation_rec.hotel_id = hotel_rec

        # Ссылка на Тип номера Бронирования
        if 'room_type' in hz_model:
            # Получаем инфо по Типу номера Бронирования
            info_room_type = hz_model['room_type']
            # Импорт Типа номера
            room_type_rec = self.room_type_import(info_room_type)
            # Добавляем ссылку
            if item_accommodation_rec.room_type_id != room_type_rec:
                item_accommodation_rec.room_type_id = room_type_rec

        # Дата заезда
        arrival_date = hz_model['arrival_date']
        # Дата отъезда
        departure_date = hz_model['departure_date']

        # Заполнение полей
        item_accommodation_rec.update({
            # ID Брони
            'booking_id': hz_model['booking_id'],
            'arrival_date': arrival_date,
            'departure_date': departure_date,
            'quantity': hz_model['quantity'],
            'price': hz_model['price'],
            'price_total': hz_model['total'],
            'hz_last_update': datetime.datetime.now(),
        })
        return item_accommodation_rec

    # Импорт позиций Авиабилетов в Заказе
    def item_flight_import(self, hz_model):
        item_flight_rec = self.env['hotels.order.item.flight'].search([('hz_id', '=', hz_model['id'])])
        if item_flight_rec:
            # Если запись позиции Авиабилет в odoo уже есть:
            if time.mktime(item_flight_rec.hz_last_update.timetuple()) >= int(hz_model['changed']):
                # 1. Если экспорт записи в odoo был позже чем последнее обновление на Hotelzov,
                #    то обновление не требуется
                print('Обновление Авиабилет в Заказе: ' + str(item_flight_rec.name) +
                      ' не требуется')
                print('Дата odoo: ' + item_flight_rec.hz_last_update.strftime('%Y-%m-%d %H:%M:%S'))
                print('Дата hotelzov: ' +
                      datetime.datetime.fromtimestamp(int(hz_model['changed'])).strftime('%Y-%m-%d %H:%M:%S'))
                return item_flight_rec
            else:
                # 2. Иначе:
                print('Обновление Авиабилет в Заказе: ' + str(item_flight_rec.name))
        else:
            # 3. Если позиция Авиабилет в odoo отсутствует, создаём запись и заполняем hz_id
            item_flight_rec = self.env['hotels.order.item.flight'].create({'hz_id': int(hz_model['id'])})
            print('Добавлено Авиабилет в Заказ, id: ' + str(hz_model['id']))
        # Для пуктов 2 и 3 обновление всех остальных полей

        # Заполнение полей
        item_flight_rec.update({
            'name': hz_model['label'],
            'quantity': hz_model['quantity'],
            'price': hz_model['price'],
            'price_total': hz_model['total'],
            'hz_last_update': datetime.datetime.now(),
        })
        return item_flight_rec

    # Импорт позиций Жел. дор. билетов в Заказе
    def item_train_import(self, hz_model):
        return

    # Импорт Заказа из Hotelzov
    def order_import(self, hz_model):
        order_rec = self.env['hotels.order'].search([('hz_id', '=', hz_model['id'])])
        if order_rec:
            # Если запись Заказа в odoo уже есть:
            if time.mktime(order_rec.hz_last_update.timetuple()) >= int(hz_model['changed']):
                # 1. Если экспорт записи в odoo был позже чем последнее обновление на Hotelzov,
                #    то обновление не требуется
                print('Обновление Заказа: ' + order_rec.name + ' не требуется')
                print('Дата odoo: ' + order_rec.hz_last_update.strftime('%Y-%m-%d %H:%M:%S'))
                print('Дата hotelzov: ' +
                      datetime.datetime.fromtimestamp(int(hz_model['changed'])).strftime('%Y-%m-%d %H:%M:%S'))
                return order_rec
            else:
                # 2. Иначе обновляем пока только Номер
                order_rec.update({'name': hz_model['number']})
                print('Обновление Заказа: ' + order_rec.name)
        else:
            # 3. Если Заказ в odoo отсутствует, создаём запись и заполняем hz_id и Номер
            order_rec = self.env['hotels.order'].create({'hz_id': int(hz_model['id']),
                                                         'name': hz_model['number']})
            print('Добавлен Заказ: ' + order_rec.name)
        # Для пуктов 2 и 3 обновление всех остальных полей
        currency_id = self.env['res.currency'].search([('name', '=', hz_model['currency_code'])]).id
        if currency_id:
            # Если id валюты найден по коду из Hotelzov (RUB, USD, ...), то обновляем
            order_rec.update({'currency_id': currency_id})
        else:
            print('Заказ: ' + order_rec.name + ' НЕ НАЙДЕН КОД ВАЛЮТЫ ИЗ HOTELZOV: ' + hz_model['currency_code'])
            print('Код валюты устоновится по умолчанию для текущей компании! ' +
                  self.env['user.company_id.currency_id'].name)
            # Сохраняем неизвестный код валюты в спец. поле
            order_rec.update({'hz_currency_code': hz_model['currency_code']})

        if 'guest' in hz_model:
            hz_guest = hz_model['guest']
            # Импорт Гостя
            guest_rec = self.guest_import(hz_guest)
            # Связываем с Гостем
            if order_rec.guest_id != guest_rec:
                order_rec.guest_id = guest_rec

        # Проверяем позиции по Заказу
        if 'order_items' in hz_model:
            hz_order_items = hz_model['order_items']
            # Если есть позиции Бронирования
            if 'roomify_accommodation_booking' in hz_order_items:
                hz_items_accommodation = hz_order_items['roomify_accommodation_booking']
                # Для каждой позиции
                for info_accommodation in hz_items_accommodation:
                    # Импортируем позицию
                    accommodation_rec = self.item_accommodation_import(info_accommodation)
                    # Устанавливаем код валюты как в Заказе
                    accommodation_rec.currency_id = order_rec.currency_id
                    # Добавляем в состав Заказа Бронирования
                    if accommodation_rec not in order_rec.item_accommodation_ids:
                        order_rec.write({'item_accommodation_ids': [(4, accommodation_rec.id, 0)]})
            # Если есть позиция на Авиа билеты
            if 'flight' in hz_order_items:
                hz_items_flight = hz_order_items['flight']
                # Для каждой позиции
                for info_flight in hz_items_flight:
                    # Импортируем позицию
                    flight_rec = self.item_flight_import(info_flight)
                    # Устанавливаем код валюты как в Заказе
                    flight_rec.currency_id = order_rec.currency_id
                    # Добавляем в состав Заказа Бронирования
                    if flight_rec not in order_rec.item_flight_ids:
                        order_rec.write({'item_flight_ids': [(4, flight_rec.id, 0)]})

        order_rec.update({
            'order_date': datetime.datetime.fromtimestamp(hz_model['date']),
            'status': hz_model['status'],
            'price': hz_model['price'],
            'hz_last_update': datetime.datetime.now(),
        })

        if order_rec:
            print('    Заказ: ' + order_rec.name + ' (Импорт завершён)')
        else:
            print('    Ошибка импорта Заказа...')
        return order_rec

    def import_info_hz(self, info):
        res = False
        if 'hotels' in info:
            info_hotels = info['hotels']
            i = 0
            for info_hotel in info_hotels:
                hotel_rec = self.hotel_import(info_hotel)
                i += 1
                print('#: ' + str(i) + '  id: ' + str(hotel_rec.id) + '  hz_id: ' + str(hotel_rec.hz_id))
                print('----------------------------------')
            res = True
        elif 'orders' in info:
            info_orders = info['orders']
            i = 0
            for info_order in info_orders:
                order_rec = self.order_import(info_order)
                i += 1
                print('#: ' + str(i) + '  id: ' + str(order_rec.id))
                print('----------------------------------')
            res = True
        else:
            print('Данные для импорта не корректны или отсутствуют!')
            res = False
        return res

    # Добавление или обновление заказа!
    def order_info_update_hz(self, arg):
        print(arg)
