# -*- coding: utf-8 -*-
import re

#stroka = 'Корм сухой Probalance Sterilized для стерилизованных кошек и кастрированных котов, с курицей, 10 кг'
def search_of_mass_product(stroka):
    try:
        if search_for_mass_composite_product_kg(stroka):
            return search_for_mass_composite_product_kg(stroka)
        elif search_for_mass_composite_product_gramm(stroka):
            return search_for_mass_composite_product_gramm(stroka)
        elif search_for_mass_in_kg(stroka):
            return search_for_mass_in_kg(stroka)
        elif search_for_mass_in_gramm(stroka):
            return search_for_mass_in_gramm(stroka)
        else:
            return 1

    except:
         print(stroka)

def search_for_mass_in_kg(stroka):
    match = re.search('\S{0,}\d{,2}\s{0,}кг', stroka)
    if match:
        return int(re.search('\d{1,}[.,]{0,1}\d*',match[0])[0].replace(',','.'))
    else:
        return 1

def search_for_mass_in_gramm(stroka):
    match = re.search('\S{0,}\d{,2}\s{0,}г', stroka)
    if match:
        return int(re.search('\d{1,}[.,]{0,1}\d*', match[0])[0].replace(',', '.'))/1000
    else:
        return 1

def search_for_mass_composite_product_gramm(stroka):
    match = re.search('\d*\s{,1}шт\S{,1}\s{,1}по\s{,1}\d{,3}\s{,1}г', stroka)
    if match:
        return int(re.search('\d*',match[0])[0]) * int(re.search('по\s{,1}\d*', match[0])[0][3:])/1000
    else:
        return 1

def search_for_mass_composite_product_kg(stroka):
    match = re.search('\d*\s{,1}шт\S{,1}\s{,1}по\s{,1}\d{,3}\s{,1}кг', stroka)
    if match:
        return int(re.search('\d*', match[0])[0]) * float(re.search('по\s{,1}\d*', match[0])[0][3:])
    else:
        return 1

if __name__ == '__main__':
    search_of_mass_product(stroka=None)