from abc import ABC, abstractmethod
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import undetected_chromedriver
import time
import sys
from selenium.webdriver.common.by import By

import new_get_mass_from_title
import re
from bs4 import BeautifulSoup
def print_to_file(text):
    with open('print.txt', 'a') as file:
        file.write(str(text))

class Browser(ABC):
    def __init__(self, reference):
        self.number_of_card_per_page = 42
        self.number_of_displayed_price_options = 5
        self.options = Browser.set_options_selenium(self)
        self.s = Service(executable_path=r'C:\chromedriver.exe')
        self.driver = undetected_chromedriver.Chrome(options=self.options, service=self.s)
        self.reference = reference
        self.list_prices_on_products = []
        self.list_titles_of_products = []
        self.list_references_of_products = []
        self.list_of_masses_products_in_kg = []
        self.cards_of_products = None

    def set_options_selenium(self):
        options = undetected_chromedriver.ChromeOptions()
        options.add_argument("--disable-blink-features")  # отключение функций блинк-рантайм
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")  # скрытый запуск браузера
        options.add_argument('--no-sandobox')  # режим песочницы
        options.add_argument('--disable-gpu')  # во избежание ошибок
        options.add_argument('--disable-dev-shm-usage')  # для увеличения памяти для хрома
        options.add_argument('--lang=en')
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/106.0.0.0 YaBrowser/22.11.5.715 Yowser/2.5 Safari/537.36')
        prefs = {"profile.managed_default_content_settings.images": 2}  # не загружаем картинки
        options.add_experimental_option('prefs', prefs)  # не загружаем картинки
        return options

    def start_selenium_browser(self):
        print('start selenium')
        self.options = Browser.set_options_selenium(self)
        self.driver = undetected_chromedriver.Chrome(options=self.options, service=self.s)
        #self.driver.get(self.reference)

    def selenium_driver_close(self):
        self.driver.close()

    def selenium_driver_quit(self):
        self.driver.quit()

    def get_soup_pagehtml(self):
        print('start soup')
        self.driver.get(self.reference)   ######### проверить
        pagehtml = self.driver.page_source
        soup = BeautifulSoup(pagehtml, 'lxml')
        return soup

    @abstractmethod
    def get_cards_of_products(self):
        pass

    @abstractmethod
    def get_link_next_page(self, i):
        pass

    @abstractmethod
    def get_price_of_product(self):
        pass

    @abstractmethod
    def get_title_of_product(self):
        pass

    @abstractmethod
    def get_reference_on_product(self):
        pass

    def get_mass_product_in_kg(self):
        for i in self.list_titles_of_products:
            self.list_of_masses_products_in_kg.append(new_get_mass_from_title.search_of_mass_product(i))
        print('self.list_of_masses_products_in_kg', 'длина', len(self.list_of_masses_products_in_kg), self.list_of_masses_products_in_kg)

    def get_price_of_product_per_kg(self,list_of_price, list_of_mass_product):
        list_prices_of_products_per_kg = []
        for i in range(len(list_of_price)):
            try:
                    price_of_product_per_kg = round(list_of_price[i] /
                                                    list_of_mass_product[i])
                    list_prices_of_products_per_kg.append(price_of_product_per_kg)
            except IndexError:
                break
        return list_prices_of_products_per_kg

    def get_basic_product_data(self):
        print('start get basic')
        self.start_selenium_browser()
        self.get_cards_of_products()
        self.get_price_of_product()
        self.get_title_of_product()
        self.get_reference_on_product()
        self.get_mass_product_in_kg()
        time.sleep(2)
        self.driver.close()

    def get_list_of_products_with_mass(self):
        print('run get_list_of_products_with_mass')
        number_of_pages_viewed = 4
        price_list_of_products = []
        # title_list_of_products = []
        # reference_list_of_product = []
        # mass_list_of_product = []
        # price_list_of_products_per_kg = []
        data_of_product = []

        self.get_basic_product_data() # собрали данные из первой страницы
        for j in range(2, number_of_pages_viewed):
            print('str124j =', j)
            self.get_link_next_page(j)
            self.get_basic_product_data() #  добавляем данные о товарах в атрибуты экземпляра
        for i in range(len(self.list_prices_on_products)):
            if type(self.list_of_masses_products_in_kg[i]) is str:
                print(' str 119 if')
                continue
            else:
                data_of_product = []
                data_of_product.append(self.get_price_of_product_per_kg(self.list_prices_on_products, self.list_of_masses_products_in_kg))
                data_of_product.append(self.list_prices_on_products[i])
                data_of_product.append(self.list_titles_of_products[i])
                data_of_product.append(self.list_references_of_products[i])
                price_list_of_products.append(data_of_product)
                print('data_of_product', data_of_product)
                #mass_list_of_product.append(self.list_of_masses_products_in_kg[i])
                #print(price_list_of_products)
        return  price_list_of_products

    # def get_price_list_of_products(self):
    #     data_of_product = []
    #     price_list_of_products = []
    #     number_of_pages_viewed = 1
    #     self.get_list_of_products_with_mass()
    #     for j in range(2, number_of_pages_viewed + 1):
    #         self.get_link_next_page(j)
    #         self.get_list_of_products_with_mass()
    #     list_prices_per_kg_or_products = self.get_price_of_product_per_kg(self.list_prices_on_products, self.list_of_masses_products_in_kg)
    #
    #     for i in range(len(self.list_titles_of_products)):
    #         try:
    #             if type(list_prices_per_kg_or_products[i]) is int:
    #
    #                 data_of_product.append((self.get_price_of_product_per_kg()))
    #                 data_of_product.append(list_prices_per_kg_or_products[i])
    #                 data_of_product.append(self.list_prices_on_products[i])
    #                 data_of_product.append(self.list_titles_of_products[i])
    #                 data_of_product.append(self.list_references_of_products[i])
    #                 price_list_of_products.append(data_of_product)
    #             else:
    #                 data_of_product.append(self.list_prices_on_products[i])
    #                 data_of_product.append(self.list_titles_of_products[i])
    #                 data_of_product.append(self.list_references_of_products[i])
    #                 price_list_of_products.append(data_of_product)
    #         except (NoSuchElementException):
    #             print('str 148 NoSuchElement or IndexError', sys.exc_info())
    #             break
    #     return price_list_of_products

    def get_dict_results_for_products(self):
        print('str174 Запускаем get_list_of_products_with_mass() из get results for products ')
        price_list_of_products = self.get_list_of_products_with_mass()
        self.dict_price_list_of_product = {}
        for i in price_list_of_products:
            if type(i[0]) is int or float:
                self.dict_price_list_of_product[i[0]] = 'руб/кг \n' + str(i[2]).strip() + '\n ' + 'Цена за единицу товара -' + \
                                            str(i[1]).strip() + ' руб.' + '\n' + str(i[3])
            else:
                self.dict_price_list_of_product[i[0]] = 'руб. за единицу товара \n' + str(i[1]) + '\n ' + \
                                                   str(i[2]) + '\n' + str(i[3])
        print('dict_price_list_of_product',self.dict_price_list_of_product)
        #return dict_price_list_of_product

    def sorting_keys_of_dict(self):
        sorting_dict = sorted(self.dict_price_list_of_product.keys())
        return sorting_dict

    def get_result_for_bot(self):
        n = 0
        result_for_bot = []
        self.get_dict_results_for_products()


        for key in self.sorting_keys_of_dict():
            n += 1
            print('№', n, str(key) + '-' + self.dict_price_list_of_product[key].translate({ord(i): " " for i in "'' ()"}))
            result_for_bot.append(('№', n, str(key) + '-' + self.dict_price_list_of_product[key].translate(
                {ord(i): " " for i in "''() "})))
            if n == self.number_of_displayed_price_options:
                break
        return result_for_bot


class ReferenceOzon(Browser):

    def get_link_next_page(self, i):
        time.sleep(3)
        if i == 2:
            match = re.search('from_global=true&', self.reference)
            self.reference = self.reference[:match.end()] + f'page={i}&' + self.reference[match.end():]
            print('self.reference i = 2 i = ', i, self.reference)
        else:
            match = re.search('page=\d', self.reference)
            self.reference = self.reference[:match.start()] + f'page={i}' + self.reference[match.end():]##self.reference[:match.start() + 5] + f'{i}' + self.reference[match.end():]
            print('next_page_reference i > 2 i =', i, self.reference)
        #self.driver.get(self.reference)

    def get_cards_of_products(self):
        print('start get cards')
        soup = ReferenceOzon.get_soup_pagehtml(self)
        self.cards_of_products = soup.find('div', class_="widget-search-result-container").find('div').find('div')

    def get_price_of_product(self):
        time.sleep(3)  #перенести в другое место
        for i in range(1, 37):
            try:
                teg_price = self.driver.find_element(By.XPATH, f'//*[@id="paginatorContent"]/div/div/div[{i}]/div[1]/div[1]/div/span[1]')
            except NoSuchElementException:
                print('get_price NoSuchElementException', i)
                teg_price = self.driver.find_element(By.XPATH, f'//*[@id="paginatorContent"]/div[1]/div/div[{i}]/div[1]/div[1]/div/span[1]')
            price_of_product = float(teg_price.text.translate({ord(i): None for i in [' ', '₽', ' ']}))
            self.cards_of_products = self.cards_of_products.find_next_sibling()
            self.list_prices_on_products.append(price_of_product)
            print('price_of_product', price_of_product)

        print("price длина = ", len(self.list_prices_on_products))

        '#paginatorContent > div.widget-search-result-container.im1 > div > div:nth-child(1) > div.ki > div.yh3.hy4.c3-a.c3-b6 > div > span.c3-a1.tsHeadline500Medium.c3-b9'

    def get_title_of_product(self):
        for i in range(1, 37):
            title_of_product = self.driver.find_element(By.XPATH, f'//*[@id="paginatorContent"]/div[1]/div/div[{i}]/div[1]/a/div/span').text
            self.list_titles_of_products.append(title_of_product)
        print('длина списка', len(self.list_titles_of_products))

    def get_reference_on_product(self):

        for i in range(1,37):
            reference_of_product = self.driver.find_element(By.XPATH, f'//*[@id="paginatorContent"]/div[1]/div/div[{i}]/div[1]/a').get_attribute("href")
            self.list_references_of_products.append(reference_of_product)

        print('длина списка reference', len(self.list_references_of_products))

### Неравномерный сбор карточек (проверить скролл), количество ссылок????
class ReferenceSber(Browser):

    def get_link_next_page(self, i):
        time.sleep(5)
        match = re.search('#\?', self.reference)
        if i == 2:
            self.reference = self.reference[:match.start()] + f'page-{i}/' + self.reference[match.start():]
        else:
            match = re.search('page-\d', self.reference)
            self.reference = self.reference[:match.start()] + f'page-{i}' + self.reference[match.end():]
        print('self.reference',self.reference)

    def get_cards_of_products(self):
        soup = ReferenceOzon.get_soup_pagehtml(self)
        self.cards_of_products = soup.select(".catalog-listing__items.catalog-listing__items_divider")[0]

    def get_price_of_product(self):
        price_teg_search = self.cards_of_products.select(".item-price")
        for i in price_teg_search:
            price_of_product = float(i.get_text().translate({ord(i): None for i in [' ', '₽', ' ']}))
            self.list_prices_on_products.append(price_of_product)
        print('длина списка', len(self.list_prices_on_products), 'price_list', self.list_prices_on_products)


    def get_reference_on_product(self):
        temporary_list_references_of_products = []
        reference_teg_search = self.cards_of_products.select('.ddl_product_link[href]')
        for i in reference_teg_search:
            reference_of_product = 'https://sbermegamarket.ru' + i['href']
            temporary_list_references_of_products.append(reference_of_product)
        for i in range(len(temporary_list_references_of_products)):
            if i % 2 == 0:
                self.list_references_of_products.append(temporary_list_references_of_products[i])
        print('длина списка reference', len(self.list_references_of_products))#,'referеnce_of_product = ',self.list_references_of_products)

    def get_title_of_product(self):
        title_teg_search = self.cards_of_products.select('.ddl_product_link[title]')
        for i in title_teg_search:
            title_of_product = i.get_text().strip()
            self.list_titles_of_products.append(title_of_product)
        print('длина списка titles', len(self.list_titles_of_products), 'list_titles_of_products = ', self.list_titles_of_products)

    def get_discont(self, card):
        try:
            discont = card.find('span', class_='bonus-amount').replace(' ', '')
        except NoSuchElementException:
            try:
                discont = card.find('span', class_='bonus-amount bonus-amount_without-percent').text.replace(' ', '')
            except NoSuchElementException:
                discont = '0'
        return discont


def main_function_get_product_data(reference):
    if reference[:16] == 'https://www.ozon':
        received_link = ReferenceOzon(reference)
    elif reference[:12] == 'https://sber':
        received_link = ReferenceSber(reference)
    else:
        return None
    number_of_pages_viewed = 3
    dict_with_collected_data = {}
    # for i in range(2, number_of_pages_viewed + 1):
    #     dict_with_collected_data = received_link.add_data_to_dict(dict_with_collected_data)
    #     print('from main', received_link.list_of_masses_products_in_kg)
    #     received_link.selenium_driver_close()
    #     received_link.start_selenium_browser()
    #     received_link.get_link_next_page(i)
    #     time.sleep(2)
    result_for_bot = received_link.get_result_for_bot()
    received_link.selenium_driver_quit()
    return result_for_bot


def test(reference):
    if reference[:16] == 'https://www.ozon':
        received_link = ReferenceOzon(reference)
    elif reference[:12] == 'https://sber':
        received_link = ReferenceSber(reference)
    else:
        return None
#   card = received_link.get_cards_of_product()
#     for i in card:
#         price = received_link.get_price(i)
#         massa = received_link.get_mass_product_in_kg(i)
#         received_link.get_price_of_product_per_kg(i)
    received_link.get_cards_of_products()
    received_link.get_title_of_product()
    received_link.get_price_of_product()
    # received_link.get_price_list_of_products()
    received_link.get_mass_product_in_kg()
    received_link.get_reference_on_product()
    # for i in received_link.list_of_masses_products_in_kg:
    #     print(i, type(i))
    # received_link.get_price_of_product_per_kg()
    # received_link.get_price_list_of_products()


if __name__ == "__main__":
    # main_function_get_product_data(reference='https://sbermegamarket.ru/catalog/korma-dlya-koshek/#?related_search='
    #                                        '%D0%BA%D0%BE%D1%80%D0%BC%D0%B0+%D0%B4%D0%BB%D1%8F'
    #                                        '+%D0%BA%D0%BE%D1%88%D0%B5%D0%BA')
    main_function_get_product_data(reference='https://www.ozon.ru/category/suhie-korma-dlya-koshek-12349/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=корм+для+кошек+сухой')
    # test('https://www.ozon.ru/category/suhie-korma-dlya-koshek-12349/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=корм+для+кошек+сухой')
