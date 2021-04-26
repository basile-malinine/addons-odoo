ОТЕЛЬ
=============
Разбираюсь с объектом Hotel. Некоторые поля доступны сразу: Наименование, Адрес, Телефон...
1. Нужны сущности: Отельер, Город, Регион (если он есть)
2. Нужно кол-во звёзд (field_hotel_stars, я так понимаю -- ссылка)
3. Нужна информация по штрафам (field_penalty_period, field_fine_amount -- тоже, наверное идентификаторы)
4. Что означает field_hotel_id? ID отеля на сайте booking

Ещё по типам комнат Hotel[types] (Object BatType):

Базовая цена это field_st_default_price[und][0][amount]?
Тип String(6) '290000' -- это базовая стоимость без десятичного разделителя?

field_st_default_price[und][0][currency] используется в системе? Кроме RUB бывет что-то ещё?


Штрафные санкции в HZ
=============
$period = array(
  ""    => "Не указано",
  "14"  => "14:00 on the day of arrival",
  "18"  =>  "18:00 on the day of arrival",
  "24"  => "until 1 days before arrival",
  "48"  => "until 2 days before arrival",
  "72"  => "until 3 days before arrival",
  "120" => "until 5 days before arrival",
)
$fine_size = array(
  ""  => "Не указано",
  "1" => "the cost of the first night",
  "2" => "50% of the total price",
  "3" => "100% of the total price",
)

Кол-во звёзд
=============
$stars = array(
  ""     => "Не указано",
  "1189" => "1 звезда",
  "876"  => "2 звезды",
  "812"  => "3 звезд",
  "828"  => "4 звезд",
  "884"  => "5 звезд",
  "1178" => "без звезд",
)

Связи объектов в Drupal
hotel[property_id] --------------------------------------- ID в Drupal отеля
hotel[field_sp_owner][und][0][target_id] ----------------- ID отельера (owner(stdClass)[uid])
hotel[field_sp_area][und][0][tid] ------------------------ ID города (city(stdClass)[tid])
hotel[property_bat_type_reference][und][0..n][target_id] - IDs типов комнат (types[0..n](BatType)[type_id])
