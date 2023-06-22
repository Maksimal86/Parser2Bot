import lxml
from bs4 import BeautifulSoup
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
import time, datetime, sys, title_massa
def options_add():
    options = webdriver.ChromeOptions()
    #options = undetected_chromedriver.ChromeOptions()
    # options.page_load_strategy = 'eager'#WebDriver ожидает, пока не будет возвращен запуск события DOMContentLoaded.
    # options.add_argument("set_window_size(0, 0)")
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    options.add_argument("--disable-blink-features")  # отключение функций блинк-рантайм
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")  # скрытый запуск браузера
    options.add_argument('--no-sandobox')  # режим песочницы
    options.add_argument('--disable-gpu')  # во избежание ошибок
    options.add_argument('--disable-dev-shm-usage')  # для увеличеня памяти для хрома
    # options.add_argument('--disable-brouser-side-navigation')  # прекращение загрузки дополниетльных подресурсов при дляительной загрузки страницы
    options.add_argument('--lang=en')
    options.add_experimental_option('useAutomationExtension',
                                    False)  # опция отключает драйвер для установки других расширений Chrome, таких как CaptureScreenshot
    # options.add_argument(
    #   '--start-maximized')  # Запускает браузер в развернутом виде, независимо от любых предыдущих настроек.
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.5.715 Yowser/2.5 Safari/537.36')  # меняем заголовок запроса
    prefs = {"profile.managed_default_content_settings.images": 2}  # не загружаем картинки
    # options.add_experimental_option('prefs', prefs)  # не загружаем картинки
    return options

def pars(ref):

    options=options_add()
    driver = webdriver.Chrome(options=options, service=s)
    driver.get(ref)
    cookies_dict = {'spid': '1674505491909_34110e1ea5d10ec177fd2bf63ed75480_i7niqkt6j33im5l0',
                    '_ym_uid': '1674505497184159621', '_ym_d': '1674505497',
                    'KFP_DID': '5a2fdeee-139f-1011-f96c-1861201b8be5',
                    'sbermegamarket_token': 'f1f61650-92de-468c-90d6-5342ee42a326',
                    'ssaid': '03b78a10-9b5c-11ed-b6f9-23b403d1bf78', 'adspire_uid': 'AS.561174187.1674505502',
                    'adtech_uid': "544fb2e5-7850-4624-89bf-6fe0e0357746%3Asbermegamarket.ru",
                    'top100_id': 't1.6795753.532073239.1674505504798', 'rrpvid': '868127971365914',
                    '_gcl_au': '1.1.1662150729.1674505517', 'rcuid': '63ceed2d6b4df55e8e25b966',
                    'flocktory-uuid': '46aab4fe-e50b-4ea7-80ee-f832a8e9a5b9-0',
                    'oxxfgh': '8d9af093-35c1-4993-9565-a582829ea163#0#7776000000#5000#1800000',
                    'analytics_session_id': 'a067ef70-82ca-467a-a7cc-595312552b13', 'isOldUser': 'true',
                    'atm_marketing': '{"id":7501,"mid":8881,"aid":"AS.561174187.1674505502","cookie_time":1674766800663,"priority":0}',
                    '_ym_isad': '1', '_gid': 'GA1.2.448029641.1675099492',
                    '_gpVisits': '{"isFirstVisitDomain":true,"todayD":"Tue Jan 31 2023","idContainer":"10002472"}',
                    '__zzatw-smm-t': 'MDA0dC0cTHtmcDhhDHEWTT17CT4VHThHKHIzd2UbN1ddHBEkWA4hPwsXXFU+NVQOPHVXLw0uOF4tbx5lTl4gSVpPCiUcE31nFRtQSxgvS18+bX0yUCs5Lmw=7GgGgQ==',
                    '_ga': 'GA1.2.1252095916.1674505503', 'last_visit': '1675154491165::1675165291165',
                    'region_info': '{"displayName":"Московская область","kladrId":"5000000000000","isDeliveryEnabled":true,"geo":{"lat":55.755814,"lon":37.617635},"id":"50"}',
                    '_gp10002472': '{"hits":7,"vc":1,"ac":1,"a6":1}', 'tmr_detect': '1|1675165297693',
                    '_ga_W49D2LL5S1': 'GS1.1.1675164574.25.1.1675165337.11.0.0', '__tld__': 'null',
                    'spsc': '1675166676762_8c3f6657c87186db159ea0552dd67cb6_a5476469b72f558bb72e6aae99c6a060',
                    'cfidsw-smm-t': 'nc8CmioBbzd/7dYYZz91dS0lvzrLqx5dQTBYbRraz3HOxvvCJ6UYCFDWIKLsK1U5hY40n7O08zhF0pj33ErBbWFRsnd4OyFhBrP04LnFW13fxN1RcB23L8yAps6qnDNJCB27k6lLhPOdjiSXi5KXwuTyxOstwX56eZPaWWNO',
                    't3_sid_6795753': 's1.1049726003.1675099491955.1675170093586.10.49'}

def sberm(ref='https://sbermegamarket.ru/catalog/?q=корм%20сухой%20для%20кошек&suggestionType=history#?filters=%7B%2288C83F68482F447C9F4E401955196697%22%3A%7B%22min%22%3A3000%2C%22max%22%3A3700%7D%2C%22B292C00B0AD3492E4150FE3EFB4B48BD%22%3A%7B%22min%22%3A10%7D%7D'):
    print('run sberMM')
    list_ref=[ref,]# Список ссылок на страницы

    list_price_kg=[]# список цен за кг
    quantly_res=5 # количество выводимых результатов
    quantly_page=3#  количество опрашиваемых страниц
    try:
        for npage in range(2, quantly_page):
            if ref[26:33] == 'catalog':
                refpage = ref[:33] + f'/page-{npage}'+ ref[33:]# первыЙ вариант ссылки через catalog
            else:
                refpage = ref + f'&page={npage}'# второй вариант через brand

            list_ref.append(refpage) # собрали все ссылки на страницы  в список

        Npage=0
        page_list=[]
        for reff in list_ref: # открываем эти ссылки  через селениум и забираем код страницы
            s = Service(executable_path=r'C:\yandexdriver.exe')
            options = options_add()
            driver = webdriver.Chrome(options=options, service=s)
            driver.get(reff)
            print(' cсылка на страницу', reff)
            time.sleep(1)
            try:
                ActionChains(driver).click(driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[1]/div[2]/div/div/div/div/div[3]/button[1]')).perform()
                print('кнопка есть')
            except:
                print('нет кнопки')
            time.sleep(1)
            page=driver.page_source
            driver.close()
            page_list.append(page) #получаем список с кодами страниц
            Npage+=1

        quantity_card=0
        res_dict = {} #С массой
        res_dict2= {} # без массы
        # забираем необходимые данные со страниц
        for page in page_list:

            with open('index.html', 'w+', encoding='utf-8', errors='ignore') as file:  # запись страницы в файл
                file.write(page)
            with open('index.html', 'r', encoding='utf=8', errors='ignore') as file:
                res=file.read()
            soup=BeautifulSoup(res, 'lxml')

            if soup.find_all('div', class_='catalog-item ddl_product catalog-item_in-enlarged-page') !=[]:
                cards =soup.find_all('div', class_='catalog-item ddl_product catalog-item_in-enlarged-page')
            elif soup.find_all('div', class_='catalog-item ddl_product')!=[]:
                cards = soup.find_all('div', class_='catalog-item ddl_product')
            elif soup.find_all('div',class_='catalog-item') !=0:
                cards= soup.find_all('div',class_='catalog-item')

            for i in cards: # здесь получаем только список карточек товаров, но не сами карточки (теги с id)
                quantity_card += 1
                try:
                    price = i.find('div', class_='item-price').text.replace(' ', '')[:-1]
                except:
                    print('except price', i.find('div', class_='item-title').text)
                ref ='https://sbermegamarket.ru'+ i.find('a').get('href')
                title = i.find('div', class_='item-title')
                try:
                    discont = i.find('span', class_='bonus-amount').get_text().replace(' ', '')
                    print('discont',discont, 'количество карточек', quantity_card)
                except:
                    print('except discont', title.text)
                    try:
                       discont = i.find('span', class_='bonus-amount bonus-amount_without-percent').text.replace(' ', '')
                    except:
                       print('except discont2', title.text)
                       discont='0'

                tuple_return=title_massa.title_m(title.text, price, discont)

                try:
                    # res_dict  для товаров с массой
                    if len(tuple_return) == 4:
                        res_dict[tuple_return[0]] = 'руб/кг\n' + tuple_return[1] + '\n '+'Цена за единицу товара -' + tuple_return[
                            2].strip() + ' руб, бонусы ' + str(tuple_return[3]) +" руб.\n"+ ref
                    else:
                        # res_dict  для штучных товаров
                        res_dict2[float(tuple_return[0])] = 'руб.\n' + tuple_return[1] +'\n'+ '   бонусы -' + tuple_return[
                            2].strip() + ' руб\n' + ref
                except:
                    print('error res_dict', sys.exc_info())
        try:
            if len(res_dict)*2>len(res_dict2):
                result=sorted(res_dict.keys())
            else:
                result = sorted(res_dict2.keys())
                res_dict=res_dict2
            #print('result', result)
        except:
            print('товаров в наличии больше нет' )
        n=0
        List_return=[]
        for key in result:
            n+=1
            #print('№', n, str(key) + '-'  + res_dict[key].translate({ord(i): " " for i in ['\xa0','"']}))
            List_return.append(('№'+ str(n)+'  '+ str(key) + '-' +res_dict[key].translate({ord(i): " " for i in ['\xa0','"']})))
            if n == quantly_res:
                break
        print('количество товаров', quantity_card)
    finally:
        driver.quit()
    return List_return

if __name__ == '__main__':
    sberm()
