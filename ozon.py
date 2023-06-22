# -*- coding: utf-8 -*-
from selenium import webdriver
import time, datetime, title_massa, sys
#from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
#import undetected_chromedriver
from selenium.webdriver.support.ui import WebDriverWait
def option_add():
    options = webdriver.ChromeOptions()
    #options = undetected_chromedriver.ChromeOptions()

    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    options.add_argument("--disable-blink-features")  # отключение функций блинк-рантайм
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless") # скрытый запуск браузера
    options.add_argument('--no-sandobox')  # режим песочницы
    options.add_argument('--disable-gpu')  # во избежание ошибок
    options.add_argument('--disable-dev-shm-usage')  # для увеличеня памяти для хрома
    options.add_argument(
        '--disable-brouser-side-navigation')  # прекращение загрузки дополниетльных подресурсов при дляительной загрузки страницы
    options.add_argument('--lang=en')
    options.add_experimental_option('useAutomationExtension',
                                    False)  # опция отключает драйвер для установки других расширений Chrome, таких как CaptureScreenshot
    options.add_argument(
        '--start-maximized')  # Запускает браузер в развернутом виде, независимо от любых предыдущих настроек.
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.5.715 Yowser/2.5 Safari/537.36')  # меняем заголовок запроса
    prefs = {"profile.managed_default_content_settings.images": 2}  # не загружаем картинки
    options.add_experimental_option('prefs', prefs)  # не загружаем картинки
    return options
def ozon(ref):
    print('run ozon')
    res_dict = {}  # словарь с результатами
    res_dict2 = {}
    list_price_kg = []  # список цен за кг
    quantly_res = 5  # количество выводимых результатов
    quantly_page = 3  # количество опрашиваемых страниц
    #url = 'https://www.ozon.ru/category/suhie-korma-dlya-sobak-12303/?brand=27604755%2C100099741%2C22426860%2C77863441&deny_category_prediction=true&from_global=true&text=корм+для+собак+сухой&weight=10000.000%3B30000.000'
   #s = Service(executable_path=r'C:\yandexdriver.exe')
    list_ref=[ref,]
    for i in range(2,quantly_page):  # получаем списки ссылок на страницы с карточками товаров
        refpage = ref[:135] + f'page={i}&' + ref[136:]
        print('ref',ref)
        list_ref.append(refpage)
        print('list_ref',list_ref)

    s = Service(executable_path=r'C:\yandexdriver.exe')
    page = 0


    for ref in list_ref:# перебираем ссылки на страницы
        page+=1
        # Получаем ссылки на карточки с товаром
        print('ozon url', 'page ',page, ref)
        options = option_add()
        driver = webdriver.Chrome(options=options, service=s)
        # заходим на каждую страницу и забираем ссылки на карточки
        driver.get(ref)
        time.sleep(1)

        for teg in range(1,37):  # собираем названия товаров
            try:
                title=driver.find_element(By.XPATH, f'//*[@id="layoutPage"]/div[1]/div[2]/div[2]/div[2]/div[6]/div[1]/div[1]/div/div[{teg}]/div[1]/a/span/span')
            except:
                print("карточек больше нет")
                break
            if str(title.text).lower().find('10кг') >= 0 or str(title).lower().find('10 кг') >= 0:
                massa = 10
            elif str(title.text).lower().find('13кг') >= 0 or str(title).lower().find('13 кг') >= 0:
                massa = 13
            else:
                massa = 15
            refs=driver.find_element(By.XPATH,f'//*[@id="layoutPage"]/div[1]/div[2]/div[2]/div[2]/div[6]/div[1]/div[1]/div/div[{teg}]/a').get_attribute("href")

            try:
                price=driver.find_element(By.XPATH,f'//*[@id="layoutPage"]/div[1]/div[2]/div[2]/div[2]/div[6]/div[1]/div[1]/div/div[{teg}]/div[1]/div[1]/div[1]').text.translate({ord(i): None for i in [' ', '₽', ' '] })
            except:
                price=driver.find_element(By.XPATH,f'//*[@id="layoutPage"]/div[1]/div[2]/div[2]/div[2]/div[6]/div[1]/div[1]/div/div[{teg}]/div[1]/div[1]/span/span[1]').text.translate({ord(i): None for i in [' ', '₽', ' '] })

            if ref == 'https://www.ozon.ru/category/suhie-korma-dlya-sobak-12303/?brand=27604755%2C100099741%2C22426860%2C77863441&deny_category_prediction=true&from_global=true&text=корм+для+собак+сухой&weight=10000.000%3B30000.000':

                if str(title.text).lower().find('chappi') >= 0 or str(title).lower().find('чаппи') >= 0 or str(
                        title).lower().find(
                        'proxвост') >= 0 or str(title).lower().find('прохвост') >= 0 or str(title).lower().find('proхвост') > 0:
                    price_kg = round(int(price.translate({ord(i): " " for i in ' '}).replace(' ', '').replace('₽', '')[:4]) / massa)
                    # создаем словарь с нужными данными
                #    card[str(price_kg) + 'руб/кг'] = title.text + str((price.translate({ord(i): " " for i in ' '})).encode('ASCII', 'ignore'))[1:]+'руб' + refs
            else:
                price_kg = round(int(price.translate({ord(i): " " for i in ' '}).replace(' ', '').replace('₽', '')[:4]) / massa)
                # создаем словарь с нужными данными
               #card[str(price_kg) + 'руб/кг'] = title.text + str((price.translate({ord(i): " " for i in ' '})).encode('ASCII', 'ignore'))[1:] + ' руб ' + refs

            tuple_return = title_massa.title_m(title.text, price, discont='0')

            try:
                ## res_dict  для товаров с массой
                    if len(tuple_return) == 4:
                        res_dict[tuple_return[0]] = 'руб/кг\n' + tuple_return[1] + '\n '+'Цена за единицу товара -' + tuple_return[
                            2].strip() + ' руб., бонусы ' + str(tuple_return[3]) +" руб.\n"+ refs
                    else:
                        # res_dict  для штучных товаров
                        res_dict2[float(tuple_return[0])] = 'руб\n' + tuple_return[1] +'\n'+ '   бонусы -' + tuple_return[
                            2].strip() + ' руб\n' + refs
            except:
                print('error res_dict', sys.exc_info())


        driver.close()
        driver.quit()
    try:  # возможно этот фрагмент надо будет добавить????
        if len(res_dict)*2 > len(res_dict2):
            result = sorted(res_dict.keys())
        else:
            result = sorted(res_dict2.keys())
            res_dict = res_dict2
    except:
        print('keys', res_dict.keys())
        print(sys.exc_info())

    n=0
    ozon_return=[]
    for key in result:
        n+=1
        print('№', n, str(key) + '-' + res_dict[key].translate({ord(i): " " for i in "'' "}))
        ozon_return.append (('№'+ str(n)+'   '+ str(key) + '-' + res_dict[key].translate({ord(i): " " for i in "'' "})))
        if n==quantly_res:
            break
    return ozon_return

        #refs= block.find_elements(By.TAG_NAME,'a')# получили все   ссылки на карточки товаров на странице



if __name__=='__main__':
    ozon(ref='https://www.ozon.ru/category/suhie-korma-dlya-koshek-12349/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=корм+для+кошек+сухой')