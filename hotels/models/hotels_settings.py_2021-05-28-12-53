from odoo import api, fields, models
import requests


class Company(models.Model):
    _inherit = 'res.company'

    # URL-адрес HZ
    url_hz = fields.Char()
    # is_test_url_pressed == true, если нажали кнопку TEST для проверки url_hz
    is_test_url_pressed = fields.Boolean()
    # is_url_ok == true, если последняя проверка соединения с url_hz была успешной
    is_url_ok = fields.Boolean()

    # Настройки подключения к odoo для передачи HZ
    odoo_url = fields.Char(default='http://95.165.247.173:8069')
    odoo_db = fields.Char(default='hotelzov')
    odoo_user = fields.Char(default='admin')
    odoo_pass = fields.Char(default='admin')

    # Номер первой записи в табл. Отелей HZ, с которой начнётся следующий экспорт/импорт
    hotels_start_record = fields.Integer()
    # Кол-во записей для след. пакета экспорта/импорта Отелей
    num_hotels_in_paket = fields.Integer()
    # Принудительное обновление Отелей
    hotels_forced_update = fields.Boolean(default=False)
    # is_hotels_import_pressed == true, если нажали кнопку IMPORT для Отелей
    is_hotels_import_pressed = fields.Boolean()

    # Номер первой записи в табл. Заказов HZ, с которой начнётся следующий экспорт/импорт
    orders_start_record = fields.Integer()
    # Кол-во записей для след. пакета экспорта/импорта Заказов
    num_orders_in_paket = fields.Integer()
    # Принудительное обновление Заказов
    orders_forced_update = fields.Boolean(default=False)
    # is_orders_import_pressed == true, если нажали кнопку IMPORT для Заказов
    is_orders_import_pressed = fields.Boolean()


class HotelsSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    odoo_url = fields.Char(default=lambda self: self.env.user.company_id.odoo_url)
    odoo_db = fields.Char(default=lambda self: self.env.user.company_id.odoo_db)
    odoo_user = fields.Char(default=lambda self: self.env.user.company_id.odoo_user)
    odoo_pass = fields.Char(default=lambda self: self.env.user.company_id.odoo_pass)

    url_hz = fields.Char(default=lambda self: self.env.user.company_id.url_hz)
    is_url_ok = fields.Char(default=lambda self: self.env.user.company_id.is_url_ok)

    hotels_start_record = fields.Integer(default=lambda self: self.env.user.company_id.hotels_start_record)
    num_hotels_in_paket = fields.Integer(default=lambda self: self.env.user.company_id.num_hotels_in_paket)
    hotels_forced_update = fields.Boolean(default=lambda self: self.env.user.company_id.hotels_forced_update)

    orders_start_record = fields.Integer(default=lambda self: self.env.user.company_id.orders_start_record)
    num_orders_in_paket = fields.Integer(default=lambda self: self.env.user.company_id.num_orders_in_paket)
    orders_forced_update = fields.Boolean(default=lambda self: self.env.user.company_id.orders_forced_update)

    @api.onchange('url_hz')
    def _onchange_url_hz(self):
        self.env.user.company_id.url_hz = self.url_hz
        # Кнопка TEST CONNECTION нажата?
        if not self.env.user.company_id.is_test_url_pressed:
            return
        else:  # Проверяем соединение с HZ
            self.test_hz_cn(self.url_hz)
            self.env.user.company_id.is_test_url_pressed = False

    def test_hz_cn_press(self):
        self.env.user.company_id.is_test_url_pressed = True

    # Тест соединения с HZ
    def test_hz_cn(self, url):
        try:
            resp = requests.post(url, data={'odoo_url': self.odoo_url,
                                            'odoo_db': self.env.cr.dbname,
                                            'odoo_user': self.odoo_user,
                                            'odoo_pass': self.odoo_pass,
                                            'entity': 'test'})
        except Exception:
            print('Error!')
            self.is_url_ok = False
        else:
            if resp.json()['status']:
                print(resp)
                self.is_url_ok = True
            else:
                print('Error!')
                self.is_url_ok = False

    @api.onchange('is_url_ok')
    def _onchange_is_url_ok(self):
        self.env.user.company_id.is_url_ok = self.is_url_ok

    @api.onchange('odoo_url', 'odoo_user', 'odoo_pass')
    def _onchange_odoo_fields(self):
        self.env.user.company_id.odoo_url = self.odoo_url
        self.env.user.company_id.odoo_user = self.odoo_user
        self.env.user.company_id.odoo_pass = self.odoo_pass

    @api.onchange('num_hotels_in_paket', 'hotels_start_record', 'hotels_forced_update')
    def _onchange_hotels_import(self):
        self.env.user.company_id.num_hotels_in_paket = self.num_hotels_in_paket
        self.env.user.company_id.hotels_start_record = self.hotels_start_record
        self.env.user.company_id.hotels_forced_update = self.hotels_forced_update
        # Кнопка IMPORT для Отелей нажата?
        if not self.env.user.company_id.is_hotels_import_pressed:
            return
        else:  # Запуск импорта Отелей
            self.import_hotels()
            self.env.user.company_id.is_hotels_import_pressed = False

    def hotels_import_press(self):
        self.env.user.company_id.is_hotels_import_pressed = True

    # Импорт Отелей
    def import_hotels(self):
        if not self.hotels_start_record:
            self.hotels_start_record = 0
        try:
            resp = requests.post(self.url_hz,
                                 data={
                                     'odoo_url': self.odoo_url, 'odoo_db': self.env.cr.dbname,
                                     'odoo_user': self.odoo_user, 'odoo_pass': self.odoo_pass, 'entity': 'hotels',
                                     'num': self.num_hotels_in_paket, 'start': self.hotels_start_record,
                                     'exp': int(self.hotels_forced_update)
                                 })
        except:
            print('Зарос <request.post(' + self.url_hz + '/oda/action...)> вызвал исключение!')
        else:
            try:
                # Если ответ "адекватный", типа: {'status': true, 'rec_count': integer}
                if 'status' in resp.json() and resp.json()['status']:
                    # Если кол-во записей вернулось меньше, чем запрашивалось -- достигли конца таблицы
                    if 'rec_count' in resp.json() and int(resp.json()['rec_count']) < self.num_hotels_in_paket:
                        # обнуляем позицию стартовой строки для импорта
                        self.hotels_start_record = 0
                    else:
                        self.hotels_start_record += self.num_hotels_in_paket
                    self.env.user.company_id.hotels_start_record = self.hotels_start_record
                else:
                    print('Ошибка, ответ от сервера: ' + str(resp))
            except:
                print('Некорректный формат ответа: ' + str(resp))

    @api.onchange('num_orders_in_paket', 'orders_start_record', 'orders_forced_update')
    def _onchange_orders_import(self):
        self.env.user.company_id.num_orders_in_paket = self.num_orders_in_paket
        self.env.user.company_id.orders_start_record = self.orders_start_record
        self.env.user.company_id.orders_forced_update = self.orders_forced_update
        # Кнопка IMPORT для Заказов нажата?
        if not self.env.user.company_id.is_orders_import_pressed:
            return
        else:  # Запуск импорта Заказов
            self.import_orders()
            self.env.user.company_id.is_orders_import_pressed = False

    def orders_import_press(self):
        self.env.user.company_id.is_orders_import_pressed = True

    # Импорт Заказов
    def import_orders(self):
        if not self.orders_start_record:
            self.orders_start_record = 0
        try:
            resp = requests.post(self.url_hz,
                                 data={
                                     'odoo_url': self.odoo_url, 'odoo_db': self.env.cr.dbname,
                                     'odoo_user': self.odoo_user, 'odoo_pass': self.odoo_pass, 'entity': 'orders',
                                     'num': self.num_orders_in_paket, 'start': self.orders_start_record,
                                     'exp': int(self.orders_forced_update)
                                 })
        except:
            print('Зарос <request.post(' + self.url_hz + '/oda/action...)> вызвал исключение!')
        else:
            try:
                # Если ответ "адекватный", типа: {'status': true, 'rec_count': integer}
                if 'status' in resp.json() and resp.json()['status']:
                    # Если кол-во записей вернулось меньше, чем запрашивалось -- достигли конца таблицы
                    if 'rec_count' in resp.json() and int(resp.json()['rec_count']) < self.num_orders_in_paket:
                        # обнуляем позицию стартовой строки для импорта
                        self.orders_start_record = 0
                    else:
                        self.orders_start_record += self.num_orders_in_paket
                    self.env.user.company_id.orders_start_record = self.orders_start_record
                else:
                    print('Ошибка, ответ от сервера: ' + str(resp))
            except:
                print('Некорректный формат ответа: ' + str(resp))
