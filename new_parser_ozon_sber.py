from abc import ABC, abstractmethod
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver
import time, sys, new_get_mass_from_title, re
from bs4 import BeautifulSoup


class Browser(ABC):
    def __init__(self, reference):
        self.number_of_card_per_page = 36
        self.number_of_displayed_price_options = 5
        self.options = Browser.set_options_selenium(self)
        self.s = Service(executable_path=r'C:\chromedriver.exe')
        self.driver = undetected_chromedriver.Chrome(options=self.options, service=self.s)
        self.reference = reference
        self.list_prices_on_products = []
        self.list_titles_of_products = []
        self.list_references_of_products = []
        self.list_prices_of_products_per_kg = []


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
        self.options = Browser.set_options_selenium(self)
        self.driver = undetected_chromedriver.Chrome(options=self.options, service=self.s)
        self.driver.get(self.reference)



    def selenium_driver_close(self):
        self.driver.close()

    def selenium_driver_quit(self):
        self.driver.quit()

    def get_soup_pagehtml(self):
        self.driver.get(self.reference)   ######### проверить
        pagehtml = self.driver.page_source
        soup = BeautifulSoup(pagehtml, 'lxml')
        return soup

    @abstractmethod
    def get_cards_of_products(self):
        pass

    @abstractmethod
    def get_next_page(self, i):
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
        self.list_of_masses_products_in_kg = []
        for i in self.list_titles_of_products:
            self.list_of_masses_products_in_kg.append(new_get_mass_from_title.search_of_mass_product(i))
            print('massa =', self.list_of_masses_products_in_kg )

    def get_price_of_product_per_kg(self):
        for i in range(self.number_of_card_per_page):
            try:
                print('self.list_of_masses_products_in_kg[i] = ', self.list_of_masses_products_in_kg[i])
                try:
                    price_of_product_per_kg =round( self.list_prices_on_products[i] / self.list_of_masses_products_in_kg[i])
                except TypeError:
                    print('TypeError', self.list_of_masses_products_in_kg[i])
                    continue
                self.list_prices_of_products_per_kg.append(price_of_product_per_kg)
                print('price_of_product_per_kg=', price_of_product_per_kg)
            except IndexError:
                break

    def get_price_list_of_products(self):
        data_of_product = []
        price_list_of_products = []
        self.get_cards_of_products()
        self.get_price_of_product()
        self.get_title_of_product()
        self.get_reference_on_product()
        self.get_mass_product_in_kg()
        self.get_price_of_product_per_kg()
        for i in range(self.number_of_card_per_page):
            try:
                if self.list_prices_of_products_per_kg[i] is None:
                    print('str 159 None per_kg')
                    continue
                else:
                    data_of_product.append(self.list_prices_of_products_per_kg[i])
                    data_of_product.append(self.list_titles_of_products[i])
                    data_of_product.append(self.list_prices_on_products[i])
                    data_of_product.append(self.list_references_of_products[i])
                    price_list_of_products.append(data_of_product)
                    data_of_product = []
            except (NoSuchElementException, IndexError):
                print('str 169 NoSuchElement or IndexError', sys.exc_info())
                break
        return price_list_of_products

    def get_dict_results_for_products(self):
        price_list_of_products = self.get_price_list_of_products()
        dict_price_list_of_product = {}
        for i in price_list_of_products:
            if i[0]:   # проверка на наличие массы продукта   исправить
                dict_price_list_of_product[i[0]] = 'руб/кг \n' + str(i[1]) + '\n ' + 'Цена за единицу товара -' + \
                                            str(i[2]).strip() + ' руб.' +'\n' + str(i[3])
            else:
                ######### доделать товары без массы
                print('str89 else')
                dict_price_list_of_product[float(i[1])] = 'руб\n' + str(i[2]) + '\n' + str(i[3])
        return dict_price_list_of_product

    def add_data_to_dict(self, dict_with_collected_data):
        print('run add_data_to_dict')
        dict_with_collected_data.update(self.get_dict_results_for_products())
        return dict_with_collected_data

    def sorting_keys_of_dict(self, dict_with_collected_data ):
        return sorted(self.add_data_to_dict(dict_with_collected_data).keys())

    def get_result_for_bot(self, dict_with_collected_data):
        n = 0
        result_for_bot = []
        for key in self.sorting_keys_of_dict(dict_with_collected_data):
            n += 1
            print('№', n, str(key) + '-' + dict_with_collected_data[key].translate({ord(i): " " for i in "'' ()"}))
            result_for_bot.append(('№', n, str(key) + '-' + dict_with_collected_data[key].translate({ord(i): " " for i in "''() "})))
            if n == self.number_of_displayed_price_options:
                break
        return result_for_bot

class Reference_Ozon(Browser):

    def get_next_page(self,i):
        time.sleep(3)
        if i == 2:
            match = re.search('from_global=true&', self.reference)
            self.reference = self.reference[:match.end()] + f'page={i}&' + self.reference[match.end():]
        else:
            match = re.search('page=\d', self.reference)
            self.reference = self.reference[:match.start()] + f'page={i}' + self.reference[match.end():]
        print('next_page_reference :', self.reference)
        self.driver.get(self.reference)



    def get_cards_of_products(self):
        soup = Reference_Ozon.get_soup_pagehtml(self)
        self.cards_of_products = soup.select(".widget-search-result-container")[0]

    def get_price_of_product(self):
        self.list_prices_on_products = []
        price_teg_search = self.cards_of_products.select( ".tsHeadline500Medium")
        for i in price_teg_search:
            price_of_product = float(i.get_text().translate({ord(i): None for i in [' ', '₽', ' '] }))
            print("price = ", price_of_product)
            self.list_prices_on_products.append(price_of_product)

    def get_title_of_product(self):
        self.list_titles_of_products = []
        title_teg_search = self.cards_of_products.select('.tsBody500Medium')
        for i in title_teg_search:
            title_of_product = i.get_text()
            print('title_of_product = ', title_of_product)
            self.list_titles_of_products.append(title_of_product)

    def get_reference_on_product(self):
        self.temporary_list_references_of_products = []
        self.list_references_of_products = []
        reference_teg_search = self.cards_of_products.select('a[href^="/product"].tile-hover-target')
        for i in reference_teg_search:
            reference_of_product ='https://www.ozon.ru' + i['href']
            print('referеnce_of_product = ', reference_of_product)
            self.temporary_list_references_of_products.append(reference_of_product)
        for i in range(len(self.temporary_list_references_of_products) - 1): #72
            if i % 2  == 0:
                self.list_references_of_products.append(self.temporary_list_references_of_products[i]) #48


class Reference_Sber(Browser):

    # def get_soup_pagehtml(self):
    #     # try:
    #     #     ActionChains(self.driver).click(self.driver.find_element(By.XPATH,
    #     #                         '/html/body/div[1]/div[1]/div[1]/div[2]/div/div/div/div/div[3]/button[1]')).perform()
    #     #     print('кнопка есть')
    #     # except:
    #     #     print('нет кнопки')
    #     pagehtml = self.driver.page_source
    #     soup = BeautifulSoup(pagehtml, 'lxml')
    #     return soup


    def get_next_page(self, i):
        time.sleep(5)
        match = re.search('#\?', self.reference)
        if i == 2:
            self.reference = self.reference[:match.start()] + f'page-{i}/' + self.reference[match.start():]
        else:
            match = re.search('page-\d', self.reference)
            self.reference = self.reference[:match.start()] + f'page-{i}' + self.reference[match.end():]
        self.driver.get(self.reference)
        print(self.reference)

    def get_cards_of_products(self):
        soup = Reference_Ozon.get_soup_pagehtml(self)
        self.cards_of_products = soup.select(".catalog-listing__items.catalog-listing__items_divider")[0]

    def get_price_of_product(self):
        self.list_prices_on_products = []
        price_teg_search = self.cards_of_products.select(".item-price")
        for i in price_teg_search:
            price_of_product = float(i.get_text().translate({ord(i): None for i in [' ', '₽', ' '] }))
            print("price = ", price_of_product)
            self.list_prices_on_products.append(price_of_product)

    def get_reference_on_product(self):
        self.temporary_list_references_of_products = []
        self.list_references_of_products = []
        reference_teg_search = self.cards_of_products.select('.ddl_product_link[href]')
        for i in reference_teg_search:
            reference_of_product ='https://sbermegamarket.ru' + i['href']
            self.temporary_list_references_of_products.append(reference_of_product)
        for i in range(len(self.temporary_list_references_of_products) - 1): #72
            if i % 2 == 0:
                self.list_references_of_products.append(self.temporary_list_references_of_products[i])
                print('referеnce_of_product = ',self.list_references_of_products)

    def get_title_of_product(self):
        self.list_titles_of_products = []
        title_teg_search = self.cards_of_products.select('.ddl_product_link[title]')
        for i in title_teg_search:
            title_of_product = i.get_text().strip()
            print('title_of_product = ', title_of_product)
            self.list_titles_of_products.append(title_of_product)

    def get_discont(self,card):
        try:
            discont = card.find('span', class_='bonus-amount').replace(' ', '')
        except:
            try:
                discont = card.find('span', class_='bonus-amount bonus-amount_without-percent').text.replace(' ', '')
            except:
                discont = '0'
        return discont

def main_function_get_product_data(reference):
    if reference[:16] == 'https://www.ozon':
        received_link = Reference_Ozon(reference)
    elif reference[:12] == 'https://sber':
        received_link=Reference_Sber(reference)
    else:
        return None
    number_of_pages_viewed = 4
    dict_with_collected_data = {}
    for i in range(2, number_of_pages_viewed + 1):
        dict_with_collected_data = received_link.add_data_to_dict(dict_with_collected_data)
        received_link.selenium_driver_close()
        received_link.start_selenium_browser()
        received_link.get_next_page(i)
        time.sleep(2)
    result_for_bot = received_link.get_result_for_bot(dict_with_collected_data)
    received_link.selenium_driver_quit()
    return result_for_bot

def test(reference):
    if reference[:16] == 'https://www.ozon':
        received_link = Reference_Ozon(reference)
    elif reference[:12] == 'https://sber':
        received_link = Reference_Sber(reference)
    else:
        return None
    #card = received_link.get_cards_of_product()
    # for i in card:
    #     price = received_link.get_price(i)
    #     massa = received_link.get_mass_product_in_kg(i)
    #     received_link.get_price_of_product_per_kg(i)
    #     print('massa = ', massa, 'price =', price, 'цена за кг -',   received_link.price_of_product_per_kg, '\n', received_link.get_reference_on_product(i))
    received_link.get_cards_of_products()
    # received_link.get_title_of_product()
    # received_link.get_price_of_product()
    # #received_link.get_price_list_of_products()
    # received_link.get_mass_product_in_kg()
    # received_link.get_price_of_product_per_kg()
    received_link.get_price_list_of_products()
#
if __name__ == "__main__":
    main_function_get_product_data(reference = 'https://sbermegamarket.ru/catalog/korma-dlya-koshek/#?related_search=%D0%BA%D0%BE%D1%80%D0%BC%D0%B0+%D0%B4%D0%BB%D1%8F+%D0%BA%D0%BE%D1%88%D0%B5%D0%BA')
    #main_function_get_product_data(reference='https://www.ozon.ru/category/suhie-korma-dlya-koshek-12349/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=корм+для+кошек+сухой')
    #test('https://sbermegamarket.ru/catalog/korma-dlya-koshek/#?related_search=%D0%BA%D0%BE%D1%80%D0%BC%D0%B0+%D0%B4%D0%BB%D1%8F+%D0%BA%D0%BE%D1%88%D0%B5%D0%BA')
