import telebot
from telebot import types
import requests


config = {
    'Name': "HotelsBot",
    'token': '5192070553:AAEGvk7UNLpWCFuD0KoFJJgZnkkZ8eyoyiQ'
}

bot = telebot.TeleBot(config['token'])
data_base = {}


@bot.message_handler(commands=["start"])
def start_command(message):
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_lowprice = types.KeyboardButton("lowprice")
    item_highprice = types.KeyboardButton("highprice")
    item_bestdeal = types.KeyboardButton("bestdeal")
    item_history = types.KeyboardButton("history")
    item_help = types.KeyboardButton("help")
    markup_reply.add(
        item_lowprice,
        item_highprice,
        item_bestdeal,
        item_history,
        item_help
    )
    bot.send_message(message.chat.id, "Что вы хотите узнать?", reply_markup=markup_reply)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == "yes":
        count_photo = bot.send_message(call.message.chat.id, "Введите количество необходимых фотографий")
        bot.register_next_step_handler(count_photo, get_photo)
    if call.data == "no":
        data_base["Count_photo"] = "0"
        bot.send_message(call.message.chat.id, f"Вы выброли город {data_base['City']},"
                                               f" и количество отелей {data_base['Count']}"
                         )
        case(call.message)


@bot.message_handler(content_types=["text"])
def get_text(message):
    if message.text == "lowprice":
        data_base["command"] = message.text
        country = bot.send_message(message.chat.id, "Введите город")
        bot.register_next_step_handler(country, get_country)
        # lowprice(message.text)
    if message.text == "highprice":
        data_base["command"] = message.text
        country = bot.reply_to(message, "Введите город")
        bot.register_next_step_handler(country, get_country)
    if message.text == "bestdeal":
        data_base["command"] = message.text
        country = bot.reply_to(message, "Введите город")
        bot.register_next_step_handler(country, get_country)
    if message.text == "help":
        markup_reply_help = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_lowprice_help = types.KeyboardButton("lowprice_help")
        item_highprice_help = types.KeyboardButton("highprice_help")
        item_bestdeal_help = types.KeyboardButton("bestdeal_help")
        item_history_help = types.KeyboardButton("history_help")
        item_return_help = types.KeyboardButton("Назад")
        markup_reply_help.add(
            item_lowprice_help,
            item_highprice_help,
            item_bestdeal_help,
            item_history_help,
            item_return_help
        )
        bot.send_message(message.chat.id, "О какой функции вы хотите узнать?", reply_markup=markup_reply_help)
    if message.text == "lowprice_help":
        bot.send_message(message.chat.id, "lowprice это команда осуществляет вывод самых дешёвых отелей в городе")
    if message.text == "highprice_help":
        bot.send_message(message.chat.id, "highprice это команда осуществляет вывод самых дешёвых отелей в городе")
    if message.text == "bestdeal_help":
        bot.send_message(message.chat.id, "bestdeal это команда осуществляет вывод самых дешёвых отелей в городе")
    if message.text == "history_help":
        bot.send_message(message.chat.id, "history это команда осуществляет вывод самых дешёвых отелей в городе")
    if message.text == "Назад":
        bot.send_message(message.chat.id, "Вы вернулись в меню", reply_markup=None)
        start_command(message)


@bot.message_handler(content_types=["text"])
def get_country(message):
    data_base["City"] = message.text
    count_hotels = bot.send_message(message.chat.id, "Введите количество отелей")
    bot.register_next_step_handler(count_hotels, get_count)


def get_count(message):
    data_base["Count"] = message.text
    check_in = bot.send_message(message.chat.id, "С какого числа вы хотите забронировать отель?")
    bot.register_next_step_handler(check_in, get_check_in)
    #


def get_check_in(message):
    data_base["check_in"] = message.text
    check_out = bot.send_message(message.chat.id, "Введите до какого числа")
    bot.register_next_step_handler(check_out, get_check_out)


def get_check_out(message):
    data_base["check_out"] = message.text
    markup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text="Да", callback_data="yes")
    item_no = types.InlineKeyboardButton(text="Нет", callback_data="no")
    markup_inline.add(
        item_yes,
        item_no
    )
    bot.send_message(message.chat.id, "Хотите ли вы фотографии", reply_markup=markup_inline)


def get_photo(message):
    data_base["Count_photo"] = message.text
    bot.send_message(message.chat.id,
                     f"Вы выброли город {data_base['City']}, количество отелей {data_base['Count']}, "
                     f"Количество фотографий {data_base['Count_photo']}")
    case(message)


@bot.message_handler(content_types=["text"])
def case(message):
    if data_base["command"] == "lowprice":
        lowprice(message)
    if data_base["command"] == "highprice":
        highprice(message)
    if data_base["command"] == "bestdeal":
        bestdeal(message)


def lowprice(message):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "3bc6638e72mshd99f94c47e42cd1p12b50fjsna4210543e3d2"
    }
    querystring = {"query": data_base["City"], "locale": "ru_RU"}
    responce = requests.request("GET", url=url, headers=headers, params=querystring)
    responce = responce.json()
    city_id = responce["suggestions"][0]["entities"][0]["destinationId"]
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": city_id,
                   "pageNumber": "1",
                   "pageSize": data_base["Count"],
                   "checkIn": data_base["check_in"],
                   "checkOut": data_base["check_out"],
                   "adults1": "1",
                   "sortOrder": "PRICE",
                   "locale": "ru_RU",
                   "currency": "RUB"
                   }
    responce = requests.request("GET",
                                url=url,
                                headers=headers,
                                params=querystring
                                )
    responce = responce.json()
    results_list = responce["data"]["body"]["searchResults"]["results"]
    for i_dict in results_list:
        hotel_id = i_dict["id"]
        hotel_name = i_dict["name"]
        hotel_address = i_dict["address"]["streetAddress"]
        distance_center = i_dict["landmarks"][0]["distance"]
        hotel_price = i_dict["ratePlan"]["price"]["current"]
        if data_base["Count_photo"] is "0":
            bot.send_message(message.chat.id,
                             f"Название отеля: {hotel_name}\n"
                             f"Адресс отеля: {hotel_address}\n"
                             f"Растояние до центра города: {distance_center}\n"
                             f"Цена за ночь: {hotel_price}"
                             )
        else:
            photo_list = []
            count_photo = int(data_base["Count_photo"])
            url_photo = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
            querystring_photo = {"id": hotel_id}
            responce_photo = requests.request("GET",
                                              url=url_photo,
                                              headers=headers,
                                              params=querystring_photo
                                              )
            responce_photo = responce_photo.json()
            bot.send_message(message.chat.id,
                             f"Название отеля: {hotel_name}\n"
                             f"Адресс отеля: {hotel_address}\n"
                             f"Растояние до центра города: {distance_center}\n"
                             f"Цена за ночь: {hotel_price}"
                             )
            for i_photo in range(count_photo):
                photo = responce_photo["hotelImages"][i_photo]["baseUrl"]
                photo = photo.replace("_{size}", "")
                photo_list.append(photo)
                bot.send_photo(message.chat.id, photo, caption=f"Фотография номер {i_photo + 1}")


def highprice(message):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "3bc6638e72mshd99f94c47e42cd1p12b50fjsna4210543e3d2"
    }
    querystring = {"query": data_base["City"], "locale": "ru_RU"}
    responce = requests.request("GET", url=url, headers=headers, params=querystring)
    responce = responce.json()
    city_id = responce["suggestions"][0]["entities"][0]["destinationId"]
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": city_id,
                   "pageNumber": "1",
                   "pageSize": data_base["Count"],
                   "checkIn": data_base["check_in"],
                   "checkOut": data_base["check_out"],
                   "adults1": "1",
                   "sortOrder": "PRICE_HIGHEST_FIRST",
                   "locale": "ru_RU",
                   "currency": "RUB"
                   }
    responce = requests.request("GET",
                                url=url,
                                headers=headers,
                                params=querystring
                                )
    responce = responce.json()
    results_list = responce["data"]["body"]["searchResults"]["results"]
    for i_dict in results_list:
        hotel_id = i_dict["id"]
        hotel_name = i_dict["name"]
        hotel_address = i_dict["address"]["streetAddress"]
        distance_center = i_dict["landmarks"][0]["distance"]
        hotel_price = i_dict["ratePlan"]["price"]["current"]
        if data_base["Count_photo"] is "0":
            bot.send_message(message.chat.id,
                             f"Название отеля: {hotel_name}\n"
                             f"Адресс отеля: {hotel_address}\n"
                             f"Растояние до центра города: {distance_center}\n"
                             f"Цена за ночь: {hotel_price}"
                             )
        else:
            photo_list = []
            count_photo = int(data_base["Count_photo"])
            url_photo = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
            querystring_photo = {"id": hotel_id}
            responce_photo = requests.request("GET",
                                              url=url_photo,
                                              headers=headers,
                                              params=querystring_photo
                                              )
            responce_photo = responce_photo.json()
            bot.send_message(message.chat.id,
                             f"Название отеля: {hotel_name}\n"
                             f"Адресс отеля: {hotel_address}\n"
                             f"Растояние до центра города: {distance_center}\n"
                             f"Цена за ночь: {hotel_price}"
                             )
            for i_photo in range(count_photo):
                photo = responce_photo["hotelImages"][i_photo]["baseUrl"]
                photo = photo.replace("_{size}", "")
                photo_list.append(photo)
                bot.send_photo(message.chat.id, photo, caption=f"Фотография номер {i_photo + 1}")


def bestdeal(message):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "3bc6638e72mshd99f94c47e42cd1p12b50fjsna4210543e3d2"
    }
    querystring = {"query": data_base["City"], "locale": "ru_RU"}
    responce = requests.request("GET", url=url, headers=headers, params=querystring)
    responce = responce.json()
    city_id = responce["suggestions"][0]["entities"][0]["destinationId"]
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": city_id,
                   "pageNumber": "1",
                   "pageSize": data_base["Count"],
                   "checkIn": data_base["check_in"],
                   "checkOut": data_base["check_out"],
                   "adults1": "1",
                   "sortOrder": "BEST_SELLER",
                   "locale": "ru_RU",
                   "currency": "RUB"
                   }
    responce = requests.request("GET",
                                url=url,
                                headers=headers,
                                params=querystring
                                )
    responce = responce.json()
    results_list = responce["data"]["body"]["searchResults"]["results"]
    for i_dict in results_list:
        hotel_id = i_dict["id"]
        hotel_name = i_dict["name"]
        hotel_address = i_dict["address"]["streetAddress"]
        distance_center = i_dict["landmarks"][0]["distance"]
        hotel_price = i_dict["ratePlan"]["price"]["current"]
        if data_base["Count_photo"] is "0":
            bot.send_message(message.chat.id,
                             f"Название отеля: {hotel_name}\n"
                             f"Адресс отеля: {hotel_address}\n"
                             f"Растояние до центра города: {distance_center}\n"
                             f"Цена за ночь: {hotel_price}"
                             )
        else:
            photo_list = []
            count_photo = int(data_base["Count_photo"])
            url_photo = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
            querystring_photo = {"id": hotel_id}
            responce_photo = requests.request("GET",
                                              url=url_photo,
                                              headers=headers,
                                              params=querystring_photo
                                              )
            responce_photo = responce_photo.json()
            bot.send_message(message.chat.id,
                             f"Название отеля: {hotel_name}\n"
                             f"Адресс отеля: {hotel_address}\n"
                             f"Растояние до центра города: {distance_center}\n"
                             f"Цена за ночь: {hotel_price}"
                             )
            for i_photo in range(count_photo):
                photo = responce_photo["hotelImages"][i_photo]["baseUrl"]
                photo = photo.replace("_{size}", "")
                photo_list.append(photo)
                bot.send_photo(message.chat.id, photo, caption=f"Фотография номер {i_photo + 1}")


bot.polling(none_stop=True, interval=0)
