from abc import ABC, abstractmethod
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver
import time, datetime, sys, new_get_mass_from_title, lxml, re
from bs4 import BeautifulSoup
class Browser(ABC):
    def set_options_selenium(self):
        #options = webdriver.ChromeOptions()
        options = undetected_chromedriver.ChromeOptions()
        #options.add_experimental_option("excludeSwitches", ['enable-automation'])
        options.add_argument("--disable-blink-features")  # отключение функций блинк-рантайм
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")  # скрытый запуск браузера
        options.add_argument('--no-sandobox')  # режим песочницы
        options.add_argument('--disable-gpu')  # во избежание ошибок
        options.add_argument('--disable-dev-shm-usage')  # для увеличеня памяти для хрома
        # options.add_argument('--disable-brouser-side-navigation')  # прекращение загрузки дополниетльных подресурсов при дляительной загрузки страницы
        options.add_argument('--lang=en')
        #options.add_experimental_option('useAutomationExtension',
        #                                False)  # опция отключает драйвер для установки других расширений Chrome, таких как CaptureScreenshot
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.5.715 Yowser/2.5 Safari/537.36')  # меняем заголовок запроса
        prefs = {"profile.managed_default_content_settings.images": 2}  # не загружаем картинки
        # options.add_experimental_option('prefs', prefs)  # не загружаем картинки
        return options
    def start_selenium_browser(self, reference):
        self.options = Browser.set_options_selenium(self)
        self.s = Service(executable_path=r'C:\yandexdriver.exe')
        self.s = Service(executable_path=r'C:\chromedriver.exe')
        #self.driver = webdriver.Chrome(options=self.options, service=self.s)
        self.driver = undetected_chromedriver.Chrome(options=self.options, service=self.s)
        self.driver.get(reference)
        page = self.driver.page_source
        with open('index.html', 'w+', encoding='utf-8', errors='ignore') as file:  # запись страницы в файл
            file.write(page)
        return self.driver

    def stop_selenium(self):
        self.driver.close()
        self.driver.quit()

    @abstractmethod
    def get_next_page(self):
        pass

    @abstractmethod
    def get_price(self, teg):
        pass

    @abstractmethod
    def get_title(self, teg):
        pass

    @abstractmethod
    def get_reference_on_product(self, teg):
        pass

    def get_price_of_product_per_kg(self, teg):
        self.massa_of_product_in_kg = new_get_mass_from_title.search_of_mass_product(
            self.get_title( teg))
        if self.massa_of_product_in_kg is None:
            return None
        else:
            try:
                self.price_of_product_per_kg = self.get_price(teg) / self.massa_of_product_in_kg
                return self.get_price(teg) / self.massa_of_product_in_kg
            except ZeroDivisionError:
                return  None

    @abstractmethod
    def get_price_list_of_products(self):
        pass
    def get_dict_results_for_products(self):
        price_list_of_products = self.get_price_list_of_products()
        dict_price_list_of_product = {}
        for i in price_list_of_products:
            if i[0]:
                dict_price_list_of_product[i[0]] = 'руб/кг \n' + str(i[1]) + '\n ' + 'Цена за единицу товара -' + \
                                            str(i[2]).strip() + ' руб.' +'\n' + str(i[3])
            else:
                ######### доделать товары без массы
                print('str89 else')
                dict_price_list_of_product[float(i[1])] = 'руб\n' + str(i[2]) + '\n' + str(i[3])
        return dict_price_list_of_product
    def add_new_data_to_dict(self, new_big_dict):
        new_big_dict.update(self.get_dict_results_for_products())
        return new_big_dict

    def sorting_keys_of_dict(self, new_big_dict ):
        return sorted(self.add_new_data_to_dict(new_big_dict).keys())

    def get_result_for_bot(self, new_big_dict):
        n = 0
        result_for_bot = []
        for key in self.sorting_keys_of_dict(new_big_dict):
            n += 1
            print('№', n, str(key) + '-' + new_big_dict[key].translate({ord(i): " " for i in "'' ()"}))
            result_for_bot.append(('№', n, str(key) + '-' + new_big_dict[key].translate({ord(i): " " for i in "''() "})))
            if n == Browser.number_of_displayed_price_options:
                break
        return result_for_bot
    number_of_displayed_price_options = 5

class Reference_Ozon(Browser):
    def __init__(self, reference):
        self.reference = reference
        self.driver = Browser.start_selenium_browser(self, reference)

    def get_next_page(self):
        try:
            try:
                self.driver.find_element(By.XPATH, '//*[@id="layoutPage"]/div[1]/div[2]/div[2]/div[2]/div[6]/div[2]/div/div[1]/div[2]/a/div/div').click()
            except NoSuchElementException:
                self.driver.find_element(By.XPATH,
                                         '//*[@id="layoutPage"]/div[1]/div[2]/div[2]/div[2]/div[5]/div[2]/div/div[1]/div[2]/a/div/div').click()
        except:
            print('get_next_page', sys.exc_info())

    def get_price(self, teg):
        try:
            return  int(self.driver.find_element(By.XPATH,f'//*[@id="paginatorContent"]/div[1]/div/div[{teg}]/div[1]/div[1]/div[1]').text.translate({ord(i): None for i in [' ', '₽', ' '] }))
        except NoSuchElementException:
            return int(self.driver.find_element(By.XPATH,
                                         f'//*[@id="paginatorContent"]/div[1]/div/div[{teg}]/div[1]/div[1]/span/span[1]').text.translate(
                {ord(i): None for i in [' ', '₽', ' ']}))

    def get_title(self, teg):
        title_product = self.driver.find_element(By.XPATH,f'//*[@id="paginatorContent"]/div[1]/div/div[{teg}]/div[1]/a/span/span[1]').text

        return title_product

    def get_reference_on_product(self, teg):
        return self.driver.find_element(By.XPATH,f'//*[@id="paginatorContent"]/div[1]/div/div[{teg}]/div[1]/a').get_attribute("href")

    def get_price_list_of_products(self):
        number_of_cards_per_page = 32
        data_of_product = []
        price_list_of_products = []
        for teg in range(1, number_of_cards_per_page):
            try:
                if Reference_Ozon.get_price_of_product_per_kg(self, teg) is None:
                    continue
                else:
                    data_of_product.append(self.price_of_product_per_kg)
                    data_of_product.append(Reference_Ozon.get_title(self, teg))
                    data_of_product.append(Reference_Ozon.get_price(self, teg))
                    data_of_product.append(Reference_Ozon.get_reference_on_product(self, teg))
                    price_list_of_products.append(data_of_product)
                    data_of_product = []

            except NoSuchElementException:
                break
        return price_list_of_products

    def add_new_data_to_dict(self, new_big_dict):
        new_big_dict.update(Reference_Ozon.get_dict_results_for_products(self))
        return new_big_dict

    def sorting_keys_of_dict(self, new_big_dict ):
        return sorted(Reference_Ozon.add_new_data_to_dict(self, new_big_dict).keys())

    number_of_displayed_price_options = 5

class Reference_Sber(Browser):
    def __init__(self, reference):
        self.reference = reference
        self.driver = Browser.start_selenium_browser(self, reference)

    def get_soup_pagehtml(self):
        try:
            ActionChains(self.driver).click(self.driver.find_element(By.XPATH,
                                                           '/html/body/div[1]/div[1]/div[1]/div[2]/div/div/div/div/div[3]/button[1]')).perform()
            print('кнопка есть')
        except:
            print('нет кнопки')
        pagehtml = self.driver.page_source
        soup = BeautifulSoup(pagehtml, 'lxml')
        return soup


    def get_next_page(self):
        ActionChains(self.driver).click(self.driver.find_element(By.CSS_SELECTOR,
                                                                '#app > main > div > div.catalog-default__container > div.catalog-default__department-container > div > div.container > div.catalog-listing-content > div.r > div.sticky-element-wrapper > div > button')).perform()

    def get_cards_of_product(self):
        soup = Reference_Sber.get_soup_pagehtml(self)
        if soup.find_all('div', class_='catalog-item ddl_product catalog-item_in-enlarged-page') != []:
            card = soup.find_all('div', class_='catalog-item ddl_product catalog-item_in-enlarged-page')
            return card

        elif soup.find_all('div', class_='catalog-item ddl_product') != []:
            card = soup.find_all('div', class_='catalog-item ddl_product')
            return card

        elif soup.find_all('div', class_='catalog-item') != 0:
            card = soup.find_all('div', class_='catalog-item')
            return card

    def get_price(self, card):
        price = card.find('div', class_='item-price').text.replace(' ', '')[:-1]
        return int(price) - int(Reference_Sber.get_discont(self, card))

    def get_reference_on_product(self, card):
        return 'https://sbermegamarket.ru' + card.find('a').get('href')

    def get_title(self, card):
        return card.find('div', class_='item-title').get_text().strip()

    def get_discont(self,card):
        try:
            discont = card.find('span', class_='bonus-amount').replace(' ', '')
        except:
            try:
                discont = card.find('span', class_='bonus-amount bonus-amount_without-percent').text.replace(' ', '')
            except:
                discont = '0'
        return discont

    def get_mass_product_in_kg(self, card):
        return new_get_mass_from_title.search_of_mass_product(Reference_Sber.get_title(self, card))

    def get_price_of_product_per_kg(self,card):
        self.massa_of_product_in_kg = Reference_Sber.get_mass_product_in_kg(self, card)
        if self.massa_of_product_in_kg is None:
            return None
        else:
            try:
                self.price_of_product_per_kg = round(self.get_price(card) / self.massa_of_product_in_kg)
                return round(self.get_price(card) / self.massa_of_product_in_kg)
            except ZeroDivisionError:
                return None

    def get_price_list_of_products(self):
        card = Reference_Sber.get_cards_of_product(self)
        data_of_product = []
        price_list_of_products = []
        for i in card:
            price = self.get_price(i)
            if Reference_Sber.get_price_of_product_per_kg(self, i) is None:
                continue
            else:
                data_of_product.append(self.price_of_product_per_kg)
                data_of_product.append(Reference_Sber.get_title(self,i))
                data_of_product.append(price)
                data_of_product.append(self.get_reference_on_product(i))
                price_list_of_products.append(data_of_product)
                data_of_product = []
        return price_list_of_products

def main_function_get_product_data(reference):
    if reference[:16] == 'https://www.ozon':
        received_link = Reference_Ozon(reference)
    elif reference[:12] == 'https://sber':
        received_link=Reference_Sber(reference)
    else:
        return None
    number_of_pages_viewed = 5
    new_big_dict = {}
    for i in range(number_of_pages_viewed):
        new_big_dict = received_link.add_new_data_to_dict(new_big_dict)
        received_link.get_next_page()
    result_for_bot = received_link.get_result_for_bot(new_big_dict)
    received_link.stop_selenium()
    return result_for_bot

def test(reference):
    received_link = Reference_Sber(reference)
    card = received_link.get_cards_of_product()
    for i in card:
        price = received_link.get_price(i)
        massa = received_link.get_mass_product_in_kg(i)
        received_link.get_price_of_product_per_kg(i)
        print('massa = ', massa, 'price =', price, 'цена за кг -',   received_link.price_of_product_per_kg, '\n', received_link.get_reference_on_product(i))

if __name__ == "__main__":
    main_function_get_product_data(reference = 'https://sbermegamarket.ru/catalog/korma-dlya-koshek/#?related_search=Корма%20для%20кошек')
#test('https://sbermegamarket.ru/catalog/korma-dlya-koshek/#?related_search=Корма%20для%20кошек')