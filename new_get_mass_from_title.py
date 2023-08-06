# -*- coding: utf-8 -*-
import re
import sys

title_of_product = 'м курицы, МКБ при мочекаменной болезни, 1шт 1.5кг '


def search_of_mass_product(title_of_product):
    try:
        if search_for_mass_composite_product_kg(title_of_product):
            print('if', title_of_product)
            return search_for_mass_composite_product_kg(title_of_product)
        elif search_for_mass_composite_product_gramm(title_of_product):
            print('elif1', title_of_product)
            return search_for_mass_composite_product_gramm(title_of_product)
        elif search_for_mass_in_kg(title_of_product):
            print('elif2', title_of_product + '/n', 'massa from new = ', search_for_mass_in_kg(title_of_product))
            return search_for_mass_in_kg(title_of_product)
        elif search_for_mass_in_gramm(title_of_product):
            print('elif3', title_of_product)
            return search_for_mass_in_gramm(title_of_product)
        else:
            print('Штучный товар ', title_of_product, type(title_of_product))#
            return title_of_product

    except:
        print('except', title_of_product, sys.exc_info())
        return None


def search_for_mass_in_kg(title_of_product):
    match = re.search('\s?\(?\d{1,3}\S{,1}\d{,3}\s{0,}кг', title_of_product)
    if match:
        return float(re.search('\d{1,}[.,]{,1}\d*', match[0])[0].replace(',', '.'))


def search_for_mass_in_gramm(title_of_product):
    match = re.search(r'\d{1,4}\s?(г|гр)\b', title_of_product)
    if match:
        return float(re.search('\(?\d{1,}[.,]{,1}\d*', match[0])[0].replace(',', '.')) / 1000


def search_for_mass_composite_product_gramm(title_of_product):
    match = re.search('\d*\s{,1}шт\S{,1}\s{,1}по\s{,1}\d{1,3}\s{,1}г', title_of_product)
    if match:
        return float(re.search('\d*',match[0])[0]) * float(re.search('по\s{,1}\d*', match[0])[0][3:])/1000


def search_for_mass_composite_product_kg(title_of_product):
    match = re.search('\d*\s{,1}шт\S{,1}\s{,1}по\s{,1}\d{1,3}\s{,1}кг', title_of_product)
    if match:
        return int(re.search('\d*', match[0])[0]) * float(re.search('\s{,1}\d*', match[0])[0][3:])

'мочекаменной болезни, 1шт 1.5кг'
if __name__ == '__main__':
    print(search_of_mass_product(title_of_product))