# -*- coding: utf-8 -*-
import re
'ой и пшеницей, 750 г  ????'
#stroka = 'Корм сухой Probalance Sterilized для стерилизованных кошек и кастрированных котов, с курицей, 10 кг'
def search_of_mass_product(stroka):
    try:
        if search_for_mass_composite_product_kg(stroka):
            print('if', stroka)
            return search_for_mass_composite_product_kg(stroka)
        elif search_for_mass_composite_product_gramm(stroka):
            print('elif1', stroka)
            return search_for_mass_composite_product_gramm(stroka)
        elif search_for_mass_in_kg(stroka):
            print('elif2', stroka)
            return search_for_mass_in_kg(stroka)
        elif search_for_mass_in_gramm(stroka):
            print('elif3',stroka)
            return search_for_mass_in_gramm(stroka)
        else:
            print('исправить re ', stroka)

    except:
        print('except', stroka)
        return None

def search_for_mass_in_kg(stroka):# ' и уткой, 10 кг'
    match = re.search('\s?\(?\d{1,3}\S{,1}\d{,3}\s{0,}кг', stroka)
    # print(match[0])
    if match:
        return float(re.search('\d{1,}[.,]{,1}\d*', match[0])[0].replace(',', '.'))

def search_for_mass_in_gramm(stroka):
    match = re.search(r'\d{1,4}\s?(г|гр)\b', stroka)
    if match:
        return float(re.search('\d*', match[0])[0]) * float(re.search('по\s{,1}\d*', match[0])[0][3:]) / 1000



def search_for_mass_composite_product_gramm(stroka):
    match = re.search('\d*\s{,1}шт\S{,1}\s{,1}по\s{,1}\d{1,3}\s{,1}г', stroka)
    if match:
        return float(re.search('\d*',match[0])[0]) * float(re.search('по\s{,1}\d*', match[0])[0][3:])/1000

def search_for_mass_composite_product_kg(stroka):
    match = re.search('\d*\s{,1}шт\s{1,}\d{1,3}\S{,1}\d{,3}\s{0,}кг', stroka)
    if match:
        return int(re.search('\d*', match[0])[0]) * float(re.search('по\s{,1}\d*', match[0])[0][3:])


if __name__ == '__main__':
    print(search_of_mass_product(stroka=' тунца и горохом для взрослых кошек 900 г'))