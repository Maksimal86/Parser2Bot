from abc import ABC, abstractmethod
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import undetected_chromedriver
import time
import sys
from selenium.webdriver.common.by import By

import new_get_mass_from_title
import re
from bs4 import BeautifulSoup


class Browser(ABC):
    def __init__(self, reference):
        self.number_of_card_per_page = 36
        self.number_of_displayed_price_options = 5
        self.options = Browser.set_options_selenium(self)
        self.s = Service(executable_path=r'C:\yandexdriver.exe')
        self.driver = webdriver.Chrome(options=self.options, service=self.s)
        self.reference = reference
        self.list_prices_on_products = []
        self.list_titles_of_products = []
        self.list_references_of_products = []
        self.list_of_masses_products_in_kg = []
        self.cards_of_products = None
        self.list_products_without_mass = []
        self.flag_of_product_with_mass = None

    def set_options_selenium(self):
        options = webdriver.ChromeOptions()
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
        self.options = Browser.set_options_selenium(self)
        self.driver = webdriver.Chrome(options=self.options, service=self.s)

    def selenium_driver_close(self):
        self.driver.close()

    def selenium_driver_quit(self):
        self.driver.quit()

    def get_soup_pagehtml(self):
        self.driver.get(self.reference)
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

    def get_price_of_product_per_kg(self,price_of_product, mass_of_product):
        if type(mass_of_product) is float or int:
            price_of_product_per_kg = round(price_of_product / mass_of_product)
            return price_of_product_per_kg
        else:
            return None

    def get_list_of_structured_data_about_products(self):
        print('run get_list_of_structured_data_about_products(self) ')
        price_list_of_products_with_mass = []
        price_list_of_products = []
        self.start_selenium_browser()
        self.get_cards_of_products()
        self.get_price_of_product()
        self.get_title_of_product()
        self.get_reference_on_product()
        self.get_mass_product_in_kg()
        for i in range(self.number_of_card_per_page):
            data_of_product = []

            try:
                print(self.list_of_masses_products_in_kg[i])
                if type(self.list_of_masses_products_in_kg[i]) is str:
                    data_of_product.append(self.list_prices_on_products[i])
                    data_of_product.append(self.list_titles_of_products[i])
                    data_of_product.append(self.list_references_of_products[i])
                    price_list_of_products.append(data_of_product)
                else:
                    data_of_product.append(
                        self.get_price_of_product_per_kg(self.list_prices_on_products[i],
                                                         self.list_of_masses_products_in_kg[i]))
                    data_of_product.append(self.list_prices_on_products[i])
                    data_of_product.append(self.list_titles_of_products[i])
                    data_of_product.append(self.list_references_of_products[i])
                    price_list_of_products_with_mass.append(data_of_product)
                    print('data_of_product, massa=', 'type', type(self.list_of_masses_products_in_kg[i]),
                          self.list_of_masses_products_in_kg[i], price_list_of_products_with_mass[i])
            except IndexError:
                print('error', sys.exc_info())
                break
        time.sleep(2)
        self.driver.close()
        if len(price_list_of_products_with_mass) > len(price_list_of_products):
            self.flag_of_product_with_mass = True
            print('price_list_of_products_with_mass', price_list_of_products_with_mass)
            return price_list_of_products_with_mass
        else:
            self.flag_of_product_with_mass = False
            print('price_list_of_products', price_list_of_products, price_list_of_products_with_mass)
            return price_list_of_products

    def get_products_data_from_different_page(self):
        number_of_pages_viewed = 4
        list_of_data_products = self.get_list_of_structured_data_about_products()
        for j in range(2, number_of_pages_viewed):
            self.get_link_next_page(j)
            list_of_data_products += self.get_list_of_structured_data_about_products()
        return list_of_data_products

    def get_dict_results_for_products(self):
        price_list_of_products = self.get_products_data_from_different_page()
        print(price_list_of_products)
        self.dict_price_list_of_product = {}
        for i in price_list_of_products:
            if self.flag_of_product_with_mass == True:
                self.dict_price_list_of_product[i[0]] = 'руб/кг \n' + str(i[2]).strip() + '\n ' + \
                                                        'Цена за единицу товара -' + \
                                            str(i[1]).strip() + ' руб.' + '\n' + str(i[3])
            else:
                self.dict_price_list_of_product[i[0]] = 'руб. за единицу товара \n' + str(i[1]) + '\n ' + str(i[2])

    def sorting_keys_of_dict(self):
        sorting_dict = sorted(self.dict_price_list_of_product.keys())
        return sorting_dict

    def get_result_for_bot(self):
        n = 0
        result_for_bot = []
        self.get_dict_results_for_products()
        for key in self.sorting_keys_of_dict():
            n += 1
            print('№', n, str(key) + '-' + self.dict_price_list_of_product[key].
                  translate({ord(i): " " for i in "'' ()"}))
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
        else:
            match = re.search('page=\d', self.reference)
            self.reference = self.reference[:match.start()] + f'page={i}' + self.reference[match.end():]

    def get_cards_of_products(self):
        ReferenceOzon.get_soup_pagehtml(self)


    def get_price_of_product(self):
        for i in range(1, 37):
            try:
                try:                    #'////*[@id="paginatorContent"]/div/div/div[2]/div[3]/div[1]/div/span[1]'
                    teg_price = self.driver.find_element(By.XPATH, f'//*[@id="paginatorContent"]/div/div/div[{i}]/div[1]/div[1]/div/span[1]')
                except:
                    print('get_price NoSuchElementException', i)
                    teg_price = self.driver.find_element(By.XPATH, f'//*[@id="paginatorContent"]/div[1]/div/div[{i}]/div[1]/div[1]/div/span[1]')
            except:
                teg_price = self.driver.find_element(By.XPATH, f'//*[@id="paginatorContent"]/div/div/div[{i}]/div[3]/div[1]/div/span[1]')
            price_of_product = float(teg_price.text.translate({ord(i): None for i in [' ', '₽', ' ']}))
            self.list_prices_on_products.append(price_of_product)


    def get_title_of_product(self):
        for i in range(1, 37):
            try:
                title_of_product = self.driver.find_element(By.XPATH, f'//*[@id="paginatorContent"]'
                                                                      f'/div[1]/div/div[{i}]/div[1]/a/div/span').text
                self.list_titles_of_products.append(title_of_product)
            except NoSuchElementException:
                title_of_product = self.driver.find_element(By.XPATH, f'//*[@id="paginatorContent"]/div/div/div[{i}]/div[2]/div/a/div/span')
    def get_reference_on_product(self):

        for i in range(1,37):
            reference_of_product = self.driver.find_element(By.XPATH, f'//*[@id="paginatorContent"]/div[1]/div/div[{i}]'
                                                                      f'/div[1]/a').get_attribute("href")
            self.list_references_of_products.append(reference_of_product)

class ReferenceSber(Browser):

    def get_link_next_page(self, i):
        time.sleep(5)
        match = re.search('#\?', self.reference)
        if match:
            if i == 2:
                self.reference = self.reference[:match.start()] + f'page-{i}/' + self.reference[match.start():]
            else:
                match = re.search('page-\d', self.reference)
                self.reference = self.reference[:match.start()] + f'page-{i}' + self.reference[match.end():]
        else:
            if i == 2:
                self.reference = self.reference + f'page-{i}/'
            else:
                print(self.reference)
                self.reference= self.reference[:-2]  + f'{i}/'

    def get_cards_of_products(self):
        soup = ReferenceOzon.get_soup_pagehtml(self)
        self.cards_of_products = soup.select(".catalog-listing__items.catalog-listing__items_divider")[0]

    def get_price_of_product(self):
        price_teg_search = self.cards_of_products.select(".item-price")
        for i in price_teg_search:
            price_of_product = float(i.get_text().translate({ord(i): None for i in [' ', '₽', ' ']}))
            self.list_prices_on_products.append(price_of_product)

    def get_reference_on_product(self):
        temporary_list_references_of_products = []
        reference_teg_search = self.cards_of_products.select('.ddl_product_link[href]')
        for i in reference_teg_search:
            reference_of_product = 'https://megamarket.ru' + i['href']
            temporary_list_references_of_products.append(reference_of_product)
        for i in range(len(temporary_list_references_of_products)):
            if i % 2 == 0:
                self.list_references_of_products.append(temporary_list_references_of_products[i])

    def get_title_of_product(self):
        title_teg_search = self.cards_of_products.select('.ddl_product_link[title]')
        for i in title_teg_search:
            title_of_product = i.get_text().strip()
            self.list_titles_of_products.append(title_of_product)


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
    elif reference[:12] == 'https://mega':
        received_link = ReferenceSber(reference)
    else:
        return None
    result_for_bot = received_link.get_result_for_bot()
    received_link.selenium_driver_quit()
    return result_for_bot


def test(reference):
    if reference[:16] == 'https://www.ozon':
        received_link = ReferenceOzon(reference)
    elif reference[:12] == 'https://mega':
        received_link = ReferenceSber(reference)
    else:
        print('none')
        return None

    received_link.get_cards_of_products()
    received_link.get_title_of_product()
    received_link.get_price_of_product()
    # received_link.get_price_list_of_products()
    received_link.get_mass_product_in_kg()
    received_link.get_reference_on_product()



if __name__ == "__main__":
    main_function_get_product_data('https://www.ozon.ru/category/smartfony-15502/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=%D1%81%D0%BC%D0%B0%D1%80%D1%82%D1%84%D0%BE%D0%BD')
