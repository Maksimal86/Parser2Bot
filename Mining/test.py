# -*- coding: utf-8 -*-
import sys
import time, datetime
from datetime import date
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import mytoken
def options_add():

    options = webdriver.ChromeOptions()
    user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) + AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')
    options.add_argument('user-agent=%s' % user_agent)
    options.add_experimental_option("excludeSwitches", ['enable-automation'])  #  FOR uc
    options.add_argument("--disable-blink-features")  # отключение функций блинк-рантайм
    options.add_argument("--disable-blink-features=AutomationControlled")
    #options.add_argument("--headless")  # скрытый запуск браузера
    options.add_argument('--no-sandobox')  # режим песочницы
    options.add_argument('--disable-gpu')  # во избежание ошибок
    options.add_argument('--disable-dev-shm-usage')  # увеличения памяти для хрома
    # options.add_argument('--disable-brouser-side-navigation')  # прекращение загрузки дополниетльных подресурсов при дляительной загрузки страницы
    options.add_argument('--lang=en')
    options.add_experimental_option('useAutomationExtension',
                                    False)  # опция отключает драйвер для установки других расширений Chrome, таких как CaptureScreenshot

    return options

def armtek_coockie():
    print('run armtek_cookie() ')
    time11 = '11:00:00'
    time00 = '00:00:00'
    time05 = '05:00:00'
    time24 = '23:59:59'
    time11obj = datetime.datetime.strptime(time11,
                                           '%H:%M:%S').time()  # перевод из строки в объект времени, беря только время
    time00obj = datetime.datetime.strptime(time00, '%H:%M:%S').time()
    time05obj = datetime.datetime.strptime(time05, '%H:%M:%S').time()
    time24obj = datetime.datetime.strptime(time24, '%H:%M:%S').time()
    timenow = datetime.datetime.now().time()
    password=mytoken.passwordarm
    login=mytoken.loginarm
    s = Service(executable_path=r'C:\yandexdriver.exe')  # расположение драйвера
    options = options_add()
    driver = webdriver.Chrome(service=s, options=options)
    url='https://etp.armtek.ru/order/report'
    driver.get(url)
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="login"]').send_keys(login)
    driver.find_element(By.XPATH,'//*[@id="authNewTemplateFormContainer"]/div/div[1]/div[2]/div/form/div[4]/div[1]/label/i[1]').click()
    driver.find_element(By.XPATH,'//*[@id="password"]').send_keys(password,Keys.ENTER)
    time.sleep(10)
    driver.refresh()
    time.sleep(2)
    kuki=driver.get_cookies()
    with open('sess.txt', 'w') as file:
        json.dump(kuki,file)
    time.sleep(10)
# ### либо armtek_cookie будет вызывать armtek
    if timenow > time11obj and timenow < time24obj:
        print('run11---00')
    elif timenow > time00obj and timenow < time05obj:
        print('run00---05')
    elif timenow > time05obj and timenow < time11obj:  # 16:22:00>05:00:00    16:22:00<11:00:00 раньше  - это меньше
        print("run05---11")
    else:
        print('str 142 где-то ошибка по времени')
#функция, которая вызывает соответствующую функцию по времени, принимает у нее данные
#  и возвращает их в вызывающую функцию - это armtek()
def time_data(): # скорее всего обойдемся без этой функции
    pass
#  функции, которые только собирают данные, вызывая data_post() и, либо записывает данные,
# либо берет из файла, дополняя своими данными, возвращает.
def data5_11(driver):
    print('run data5_11 ')
    driver.find_element(By.XPATH, '//*[@id="SCRDATE"]').clear()  # первая ячейка даты создания заказа
    driver.find_element(By.XPATH, '//*[@id="SCRDATE"]').send_keys('\uE003' * 10,
                                                                  (date.today() - datetime.timedelta(days=20)).strftime(
                                                                      "%d.%m.%Y"), Keys.ENTER)
    time.sleep(5)
    list_z=[]

    try:
        for i in range(1,10): # парсим 10 строк
            s=driver.find_element(By.XPATH, f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[12]/div').text # сумма поставки
            kom=driver.find_element(By.XPATH,f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[15]/span').text # комментарий
            try:
                date_f = driver.find_element(By.XPATH, f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[5]/div/div').text
                print(date_f)
                factura=driver.find_element(By.XPATH, f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[5]/div/a').get_attribute('href')
                print(factura)
            except:
                continue
            if (date.today() - datetime.timedelta(days=3)).strftime("%d.%m.%Y")== date_f: # сегодняшняя дата = дате поставки
                #list_z.append('Сумма: ' + s + 'руб, комментарий: ' + kom)
                print(s,'\n',kom)
                driver.get(factura)
                time.sleep(15)
                for i in range(1,15):
                    time.sleep(5)
                    try:
                        zch=driver.find_element(By.XPATH, f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[5]').text
                        print('zch',zch)
                        list_z.append(zch)


                    except:
                        print(sys.exc_info())
                        break
            print(list_z)
            return list_z
    except: # если строк в поиске < 10
        print(sys.exc_info())
        print('данных больше нет')
    print(list_z)
    return list_z
    #driver.find_element(By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[3]/td[5]/div/div/text()')
    pass


def data11_24(driver):
    print('run data11_24() ')
    list_z=data_post(driver)[:]# собрали данные по поставкам
    with open("armtek.txt", 'w') as file:
        for i in list_z:
            file.write(str(i)+'\n') #записали в файл
    return list_z
def data0_5(driver):
    print('run data0_5() ')
    list_z=data_post(driver)[:]# собрали данные по поставкам
    with open("armtek.txt", 'r') as file:
        for i in file.readlines(): # прочитали ранее записанный файл
            list_z.append(i) # в список вновь полученных поставок добавили ранее полученные поставки
    return list_z



def data_post(driver): # получаем список поставок
    print('run data post ')
    driver.find_element(By.XPATH,'//*[@id="SCRDATE"]').clear() # первая ячейка даты создания заказа
    driver.find_element(By.XPATH, '//*[@id="SCRDATE"]').send_keys('\uE003'*10,(date.today()- datetime.timedelta(days=20)).strftime("%d.%m.%Y"), Keys.ENTER)
    time.sleep(5)
    list_z=[]

    try:
        for i in range(1,10):
            s=driver.find_element(By.XPATH, f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[12]/div').text # сумма поставки
            kom=driver.find_element(By.XPATH,f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[15]/span').text # комментарий
            try:
                date_p=driver.find_element(By.XPATH,f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[4]/div/div').text
            except:
                continue
            if date.today().strftime("%d.%m.%Y") == date_p: # сегодняшняя дата = дате поставки
                try:
                    data_f=driver.find_element((By.XPATH,f'//*[@id="DataTables_Table_1"]/tbody/tr[i]/td[5]/div')).text
                except: # а фактуры нет
                    list_z.append('Сумма: ' + s + 'руб, комментарий: ' + kom)
                print(s,'\n',kom)
        return list_z
    except:
        print(sys.exc_info())
        print('Поставок больше нет')
    print(list_z)
    return list_z

def armtek():
    time11='11:00:00'
    time00='00:00:00'
    time05='05:00:00'
    time24='23:59:59'
    time11obj = datetime.datetime.strptime(time11,
                                           '%H:%M:%S').time()  # перевод из строки в объект времени, беря только время
    time00obj = datetime.datetime.strptime(time00, '%H:%M:%S').time()
    time05obj = datetime.datetime.strptime(time05, '%H:%M:%S').time()
    time24obj = datetime.datetime.strptime(time24, '%H:%M:%S').time()
    timenow = datetime.datetime.now().time()
    print(' run armtek')
    options = options_add()
    s = Service(executable_path=r'C:\yandexdriver.exe')  # расположение драйвера
    driver = webdriver.Chrome(service=s, options=options)
    url='https://etp.armtek.ru/order/report'
    driver.get(url)
    time.sleep(5)
    try:
        #driver.refresh() # перезагружаем для того, чтобы добавить куки
        time.sleep(3)
        with open('sess.txt') as sess:
            kuk=json.load(sess) # забираем куки из файла
            print(kuk)
        k=driver.get_cookies()
        print(k)
        for i in range(len(kuk)):
            driver.add_cookie({'name':kuk[i]['name'], 'value':kuk[i]['value']})
       # Куки добавляются именно так, по другому с добавлением всех элемeнтов не работает -
       # из каждого словаря из списка словарей берутся значения по ключам 'name' и 'value',
       # которые потом попадают в соответствующие словари с этими же ключами и значениями
       # остальные данные кук селениум добавляет сам.
        driver.get(url)
        time.sleep(5)
        # ##### Эта функция будет вызывать соответствующую времени функцию data...(), передавая драйвер
        # ####  Либо также через armtek_cookie()
        # ### либо armtek_cookie будет вызывать armtek
        if  timenow >time11obj and timenow < time24obj:
            return data5_11(driver)
        elif  timenow >time00obj and timenow < time05obj:
            return data5_11(driver)#data0_5(driver)
        elif  timenow >time05obj and timenow < time11obj:
            return data5_11(driver)
        else:
            print('str 142 где-то ошибка по времени')

    except:
        driver.close()
        print(sys.exc_info())
        print('armtek except')
        return armtek_coockie() # получили куки, записали в файл и вернули список с поставками
        #return data(driver)
    finally:
        driver.quit()

if __name__ == '__main__':
    armtek()


