# -*- coding: utf-8 -*-
import asyncio, os, json
import timer, tokenbot
import datetime, sys
import ozon, SberMM
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData

#dd
bot=Bot(tokenbot.tokenbot)
dp=Dispatcher(bot)
moni=1
mess_id=''
mess_ref=''
time_monitor1='10:30'
time_monitor2='19:30'
@dp.message_handler(content_types=['text'])
async def send_message(message):
    global mess_ref
    klava = InlineKeyboardMarkup(row_width=2)  # в строке по две кнопки
    but_inl1 = InlineKeyboardButton(text='Начать отслеживать', callback_data='start_inl')
    but_inl2 = InlineKeyboardButton(text='Не отслеживать', callback_data='no_inl')
    klava.add(but_inl1, but_inl2)
    but = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Dogs Chappi Ozon')
    btn2 = types.KeyboardButton('Cats ProB Ozon')
    btn3=types.KeyboardButton('Cats ProB SMM')
    btn4=types.KeyboardButton('Dogs Chappi SMM')
    btn5=types.KeyboardButton('сбор данных')
    but.add(btn1, btn2, btn3, btn4, btn5)

    if message['text'][:12] == 'https://sber' or message['text'][:16] == 'https://www.ozon':
        await bot.send_message(message.from_user.id, 'обрабатываю запрос...', reply_markup=but)
        await sbor_ozon_sber(message)
    elif message['text'] == 'Dogs Chappi Ozon':
        print(type(message))
        await bot.send_message(message.from_user.id, 'обрабатываю запрос...', reply_markup=but)
        message['text']='https://www.ozon.ru/category/korm-dlya-sobak-12302/chappi-27604755/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=чаппи'
        await sbor_ozon_sber(message)
    elif message['text'] == 'Cats ProB Ozon':
        await bot.send_message(message.from_user.id, 'обрабатываю запрос...', reply_markup=but)
        message['text']='https://www.ozon.ru/category/suhie-korma-dlya-koshek-12349/probalance-32169982/?deny_category_prediction=true&from_global=true&sorting=ozon_card_price&text=корм+для+кошек+сухой&weight=10000.000%3B36300.000'
        await sbor_ozon_sber(message)
    elif message['text'] =='Cats ProB SMM':
        await bot.send_message(message.from_user.id, 'обрабатываю запрос...', reply_markup=but)
        message['text'] ='https://sbermegamarket.ru/catalog/?q=корма%20для%20кошек%20probalance&suggestionType=brand'
        await sbor_ozon_sber(message)
    elif message['text'] =='Dogs Chappi SMM':
        await bot.send_message(message.from_user.id, 'обрабатываю запрос...', reply_markup=but)
        message['text']='https://sbermegamarket.ru/catalog/?q=чаппи'
        await sbor_ozon_sber(message)
    elif message['text'] == 'сбор данных':
        await monitor_data(message)
        await bot.send_message(message.from_user.id, 'обрабатываю запрос...', reply_markup=but)
    elif message['text'] == 'старт':
        await auto_start()
    elif message['text'] == 'кнопки':
        await bot.send_message(message.from_user.id, 'Пожалуйста, кнопки...', reply_markup=but)
    else:
        await bot.send_message(message.chat.id, 'Неизвестная \n команда')
    mess_ref = message
# Сделать так, чтобы запуск проходил 1 раз по всем файлам за 1 True из timer
async def auto_start():
    schetchik=0
    while True:
        list_files = []# список файлов со ссылками
        if await timer.timer(time_monitor1 + ':00') or await  timer.timer(time_monitor2 + ':00'):
            for root, dirs, files in os.walk("."):
                for filename in files:
                    if filename[:11] == 'monitor_ref':
                        list_files.append(filename) # собрали все файлы, связанные с отслеживанием
            for i in list_files:
                with open(i, 'r', encoding='utf-8', errors='ignore') as file:
                    mon_ref=file.readline() # получили True из monitor_ref
                    message=file.readline()#получили строку message, записанную в файл
                    #print('str76','message', message, type(message))

                if mon_ref == 'True\n' and message: # проверяем, что файл содержит True
                    schetchik += 1
                    message = json.loads(message)  # переводим строку в словарь
                    if l_ref(message['from']['id']) == []:# Файл с сылками пуст
                        print('continue')
                        continue
                    print("str79 message", message)
                    for i in l_ref(message['from']['id']):  # передали список ссылок из файла monitor_list_ref()
                        print(l_ref(message['from']['id']))
                        print('str82', message['from']['id'])
                        message['text'] = i[:-1]  # "общую" ссылку подменили  на одну из отслеживаемых ссылок
                        print('str84 запуск sbor_ozon_sber()  из auto_start ')
                        await sbor_ozon_sber(message)
                        await asyncio.sleep(60)  # задержка между опросами по ссылкам # прошлись по ссылкам из одного файла
                        print('str87 итерация for окончена')
                    print('str88 for окончен')
            print('Количество проверенных файлов=', schetchik, "большой перерыв")
            await asyncio.sleep(600)

def l_ref(userid): # возвращаем список ссылок из файла
    with open (f'monitor_list_ref{userid}.txt','a+', encoding='utf-8', errors='ignore') as file:
        file.seek(0)
        fileread=file.readlines()[:]
        return fileread

#  функция добавляет ссылку в файл со списком ссылок
async def add_l_ref(callback: types.CallbackQuery):
    with open(f'monitor_list_ref{callback["from"]["id"]}.txt', 'r+', encoding='utf-8', errors='ignore') as file:# был r+
        print('str101 ','run', callback.data)
        for st in file.readlines():
            print('str103', st)
            print('str 105 mess_ref', mess_ref)
            print('str104', mess_ref['text'] + '\n', mess_ref)
            if st == mess_ref['text'] + '\n':  # если ссылка из списка равна переданной ссылке, т.е. она уже добавлена
                print('str106 ссылка уже добавлена')
                await callback.answer('ссылка уже добавлена')
                break
            else:  # если не равна, т.е. нет в списке
                continue
        else:  # а если всё-таки равно
            if callback["from"]["id"] == mess_ref["from"]["id"]:
                file.write(str(mess_ref['text'] + '\n'))
                await callback.answer('ссылка добавлена')


async def del_l_ref(callbackid1):
    try:
        lr = []
        for st in l_ref(callbackid1):
            print('str 122 callbackid1', callbackid1)
            print('str123 mess_ref', mess_ref)
            print('str124',st)
            print('str125',mess_ref['text']+'\n')
            if st != mess_ref['text'] +'\n':
                lr.append(st)
    except:
        print('str 130 Поздно нажали "Закончить отслеживать"')
        print(str(sys.exc_info()))
    with open(f'monitor_list_ref{callbackid1}.txt', 'w', encoding='utf-8', errors='ignore') as file:

        for i in lr:
            file.write(i)

# повторный вызов последнего в списке, while сделать
async def sbor_ozon_sber(message): # функция вызвана с первой ссылкой из списка
    print('str137 run sbor...()')
    klava = InlineKeyboardMarkup(row_width=2)  # в строке по две кнопки
    but_inl1 = InlineKeyboardButton(text='Начать отслеживать', callback_data='start_inl')
    but_inl2 = InlineKeyboardButton(text='Не отслеживать', callback_data='no_inl')
    klava.add(but_inl1, but_inl2)
    print('str142 message', message)
    klava2 = InlineKeyboardMarkup(row_width=2)
    but_inl12 = InlineKeyboardButton(text='Закончить отслеживать', callback_data='finish_inl')
    but_inl22 = InlineKeyboardButton(text='Продолжить отслеживать', callback_data='no_inl2')
    klava2.add(but_inl22, but_inl12)
    schoz = 0  # счетчик количества проверенных ссылок
    schsb = 0
    if message['text'][:12] == 'https://sber':  # если боту прислали ссылку и это ссылка сбера
        list_sber = SberMM.sberm(message['text'])[:]  # создаем новый список - результат вызова функции SberMM.sberm
        if l_ref(message['from']['id']) == []:  # если в списке ссылок еще ничего нет
            print('str152, ссылка не  в списке' + str(message['text']), l_ref(message.from_user.id))
            for i in list_sber:
                await bot.send_message(message.from_user.id, str(i),
                                       reply_markup=klava)  # вызываем соответствующую инлайн клавиатуру с вопросом "начать отслеживать"
        else:  # если список не пуст
            for j in l_ref(message['from']['id']):  # проверяем вхождение текущей ссылки запроса в список проверяемых ссылок
                # для того, чтобы вызвать соответствующю  инлайн клавиатуру
                print('str159', j, message['text'])
                schsb+=1
                if message['text'] + '\n' == j:  ########## если  ссылка в списке
                    for i in list_sber:
                        await bot.send_message(message['from']['id'], str(i),
                                               reply_markup=klava2)  # вызываем клавиатуру с вопросом " закончить отслеживать"
                        print('str165 ссылка в списке ')
                    break
                elif schsb == len(l_ref(message['from']['id'])): # проверяем наличие ссылки в последнее строке списка
                    print('str168, ссылка не  в списке ' + str(message['text']), l_ref(message['from']['id']))
                    for i in list_sber:
                        await bot.send_message(message.from_user.id, i,
                                               reply_markup=klava)  # вызываем соответствующую инлайн клавиатуру с вопросом "начать отслеживать"
                else:
                    continue
    elif message['text'][:16] == 'https://www.ozon':
        list_ozon = ozon.ozon(message['text'])[:]  # создаем новый список - результат вызова функции ozon.ozon()
        if l_ref(message['from']['id']) == []:  # если в списке ссылок еще ничего нет
            print('str177, ссылка не  в списке' + str(message['text']), l_ref(message['from']['id']))
            for i in list_ozon:
                await bot.send_message(message['from']['id'], i,
                                       reply_markup=klava)  # вызываем соответствующую инлайн клавиатуру с вопросом "начать отслеживать"
        else:  # если список не пуст
            for j in l_ref(message['from']['id']):  # проверяем вхождение текущей ссылки запроса в список проверяемых ссылок
                schoz += 1
                print('str184', j, message['text'])
                if message['text'] + '\n' == j:  ################ если  ссылка в списке
                    for i in list_ozon:
                        await bot.send_message(message['from']['id'], i,
                                               reply_markup=klava2)  # вызываем клавиатуру с вопросом " закончить отслеживать"
                        print('str189 ссылка в списке\n', 'sbor_ozon_sber(message) завершена')
                    break
                elif schoz == len(l_ref(message['from']['id'])):  # проверяем, чтобы проверяемая ссылка была последней в списке
                    print('str192 ссылка не  в списке', str(message['text']), l_ref(message['from']['id']))
                    for i in list_ozon:
                        await bot.send_message(message['from']['id'], i,
                                               reply_markup=klava)  # вызываем соответствующую инлайн клавиатуру с вопросом "начать отслеживать"
                else:
                    print('str197 continue ', 'len=', len(l_ref(message['from']['id'])), 'sch=', schoz)
                    continue

async def monitor_data(message):  #получили message один из файла
    print('str201 run monitor_data', message.from_user.id, l_ref(message.from_user.id))
    if l_ref(message.from_user.id) == []:
        await bot.send_message(message.from_user.id, "Ничего не отслеживается")
        await bot.send_message(message.from_user.id, 'Добавьте ссылку для отслеживания')
    else:
        await bot.send_message(message.from_user.id, 'собираем данные по списку')
        for i in l_ref(message.from_user.id):  # передали список ссылок
            print('str208',message)
            message['text'] = i[:-1]  # подменили "сбор данных" на ссылку и убрали знак переноса
            # сюда надо передать message
            print('str211 запуск sbor_ozon_sber()  из monitor_data ')
            await sbor_ozon_sber(message)
            await asyncio.sleep(60) # задержка между опросами по ссылкам # прошлись по ссылкам из одного файла
            print('str214 итерация for окончена')
        print('str215 for окончен')



# Здесь отслеживаем все обратные вызовы
# проверка от кого пришел колбэк. id в ссылке должен совпадать c id файла
@dp.callback_query_handler()
async def start_tracking(callback: types.CallbackQuery):
    print('str223 callback', callback.data)
    if  callback.data == 'start_inl' and callback["from"]["id"] == mess_ref['from']['id']: # нажата кнопка "начать отслеживание
        await add_l_ref(callback)
        with open(f'monitor_ref{callback["from"]["id"]}.txt', 'w', encoding='utf-8', errors='ignore') as file:
            file.write('True'+'\n' + str(mess_ref))
        #await auto_start()
        await callback.answer('включаем...', )

    elif callback.data =='no_inl':  # нажатa кнопка "не отслеживать"
        await callback.answer('Ну нет - так нет!')
        #with open('monitor_ref.txt', 'w', encoding='utf-8', errors='ignore') as file:
        #    file.write('False')
        await callback.answer('Отслеживание остановлено')
    elif callback.data == 'finish_inl':# нажата кнопка "Закончить отслеживать"
        await del_l_ref(callback['from']['id'])
        await callback.answer('Этот товар больше не отслеживается')

    elif callback.data =='no_inl2':# нажата кнопка "Продолжить отслеживать"
        await callback.answer('Всё по-прежнему')


try:
    executor.start_polling(dp)  # (timeout=5, long_polling_timeout = 5)#(none_stop=True, interval=0)
except:
    with open('log.txt', 'a', encoding='utf-8') as log:
        log.write('start_polling ' + str(datetime.datetime.now()) + ' нет соединения ' + str(sys.exc_info()) + '\n')




