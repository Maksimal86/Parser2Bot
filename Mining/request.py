# -*- coding: utf-8 -*-
import sys
import asyncio
import time
import mytoken
import logging
import datetime
from aiogram import Bot, Dispatcher, executor, types
import WtoM,hashrateno2, mineros, Hive, binance, armtek,timer

righive=4
rigmineros=2

logger = logging.getLogger(__name__)
bot=Bot(mytoken.tokenbot)
dp=Dispatcher(bot)
monitor=0
@dp.message_handler(content_types=['text'])
async def send_message(message):


    but = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('хешрейт')
    btn2 = types.KeyboardButton('Старт')
    btn3 = types.KeyboardButton('Стоп')
    btn4 = types.KeyboardButton('профит')
    btn5 = types.KeyboardButton('Армтек')
    btn6 = types.KeyboardButton('binance')
    but.add(btn1, btn2, btn3, btn4, btn5, btn6)
    print(message.text.lower(), message)
    if message.text.lower() == 'хешрейт':
        #await bot.send_message(message.from_user.id, mineros.hashrate(), reply_markup=but)
        await bot.send_message(message.from_user.id, Hive.hive_hashrate(), reply_markup=but)

    elif message.text.lower() == 'старт': #запуск Wdog
        await bot.send_message(message.from_user.id, "запуск...", reply_markup=but)
        print('старт')
        global monitor
        monitor = 1
        await asyncio.gather(armtek_momitor(message),monitor_hashrate(message),delta_price(message))  # одновременный запуск асинхронных функций

    elif message.text.lower() == 'стоп':# остановка Wdog
        monitor = 0
        print(monitor)
    elif message.text.lower() == 'профит': # Парсинг hashrate.no и what to mine с выводом соответствующих данных о доходности
        if hashrateno2.error == 0:
            print(hashrateno2.error)
            await bot.send_message(message.from_user.id, 'Нет соединения с сайтом')
        elif type(WtoM.whattomine()) ==  str:
            await bot.send_message(message.from_user.id, 'Нет соединения с сайтом')
        else:
            for j in hashrateno2.hasrateno():
                await bot.send_message(message.from_user.id, str(j).translate({ord(i):None for i in "[]'" }))
            for i in WtoM.whattomine():
                await bot.send_message(message.from_user.id, i)
    elif message.text.lower() == 'армтек':
        armtek_list = armtek.armtek()[:]
        print('armtek_list', armtek_list)
        if armtek_list == []:
            await bot.send_message(message.from_user.id, 'Пока поставка не сформирована')
        else:
            for i in armtek_list:
                await bot.send_message(message.from_user.id, i)
    elif message.text == 'binance':
        for i in binance.bin():
            await bot.send_message(message.from_user.id, i)
    else:
        await bot.send_message(message.chat.id, 'Неизвестная команда')

# Наблюдение за количеcтвом ригов онлайн
async def monitor_hashrate(message):
    while monitor:
        #mineros.hashrate()
        print('monitor hashrate run', monitor)
        if Hive.save_onlinehive() < righive:
            await asyncio.sleep(0.3)
            await bot.send_message(message.from_user.id, text='Hive rig offline, online rigs = ' + str(
                Hive.save_onlinehive()))
            await asyncio.sleep(0.5)
            mineros.period=30
            with open('log.txt', 'a') as log:
                log.write('Hive' + str(datetime.datetime.now()) + 'rig offline' + str(Hive.save_onlinehive()) + '\n')
        if Hive.save_onlinehive() < righive: mineros.period=180
        await asyncio.sleep(mineros.period)

async def delta_price(message):
    try:
        while monitor:
            print('binance run', monitor)
            for i in binance.bin():
                print(i,(i[2][:-1]), float(i[2][:-1]))
                if float(i[2][:-1])>5 or float(i[2][:-1])<-5:

                    await bot.send_message(message.from_user.id, text="Изменение больше 5% "+str(i))
            await asyncio.sleep(3600)
    except:
        with open("log.txt", 'a') as log:
            log.write('delta_price '+str(datetime.datetime.now())+' '+str(sys.exc_info())+'\n')
async def armtek_momitor(message):
    time1='23:00'
    time2='01:30'
    time3='08:45'
    while True:
        if  await timer.timer(time1+ ':00') :
            armtek_list = armtek.armtek()[:]
            if armtek_list == []:
                await bot.send_message(message.from_user.id, 'Пока поставка не сформирована')
            else:
                for i in armtek_list:
                    await bot.send_message(message.from_user.id, i)
            await asyncio.sleep(600)
        elif await timer.timer(time2+ ':00'):
            armtek_list = armtek.armtek()[:]
            if armtek_list == []:
                await bot.send_message(message.from_user.id, 'Пока поставка не сформирована')
            else:
                for i in armtek_list:
                    await bot.send_message(message.from_user.id, i)
            await asyncio.sleep(600)
        elif await timer.timer(time3+ ':00'):
            armtek_list = armtek.armtek()[:]
            if armtek_list == []:
                await bot.send_message(message.from_user.id, 'Пока поставка Армтек не сформирована')
            else:
                for i in armtek_list:
                    await bot.send_message(message.from_user.id, i)
            await asyncio.sleep(600)
        else:
            print("armtek_monitor() False")

try:
    executor.start_polling(dp)#(timeout=5, long_polling_timeout = 5)#(none_stop=True, interval=0)
except:
    with open('log.txt', 'a', encoding='utf-8') as log:
        log.write('start_polling ' + str(datetime.datetime.now()) + ' нет соединения ' + str(sys.exc_info()) + '\n')
    time.sleep(2)
    executor.start_polling(dp, skip_updates=True)#(timeout=5, long_polling_timeout=5)


'''как определяется риг для выполнения команды?
ошибка replace'''


'''
ловить исключения

токена авторизации на mineros
'''