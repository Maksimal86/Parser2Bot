import time
import asyncio

async def timer(timetime):

    print(time.strftime("%X", time.localtime()), timetime)
    t=time.strftime("%X", time.localtime())
    await  asyncio.sleep(60)
    if int(t.replace(':', '')) <= int(timetime.replace(':', ''))+1000 \
            and int(t.replace(':', '')) >= int(timetime.replace(':', ''))-1000:
        print('timer return True'+timetime, t, int(timetime.replace(':', '')), int(t.replace(':', '')),int(timetime.replace(':', ''))+100, int(timetime.replace(':', ''))-100)
        return True
    else:
        print('timer return False'+timetime, t, int(timetime.replace(':', '')), int(t.replace(':', '')))


if __name__ == '__main__':
    timer(timetime='16:22:00')


# https://sbermegamarket.ru/catalog/?q=чаппи
# https://sbermegamarket.ru/brands/kitekat/#?related_search=kitekat
# https://www.ozon.ru/category/suhie-korma-dlya-koshek-12349/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=корм+для+кошек+сухой
# https://www.ozon.ru/category/suhie-korma-dlya-sobak-12303/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=корм+для+собак+сухой