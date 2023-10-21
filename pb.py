from datetime import datetime, timedelta
import platform
from datetime import datetime
import logging
import sys
import aiohttp
import asyncio


async def request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    r = await resp.json()
                    # print(r)
                    return r
                logging.error(f"Error status: {resp.status} for {url}")
                return None
        except aiohttp.ClientConnectorError as err:
            logging.error(f"Connection error: {str(err)}")
            return None


async def get_exchange(date):
    result = await request('https://api.privatbank.ua/p24api/exchange_rates?date=' + date)
    if result:
        rates = result.get('exchangeRate')
        exc1, = list(filter(lambda element: element["currency"] == "USD", rates))
        exc2, = list(filter(lambda element: element["currency"] == "EUR", rates))
        # print(exc1)
        res = {date:{'EUR':{'sale':exc2['saleRate'],'purchase':exc2['purchaseRate']},
                     'USD':{'sale':exc1['saleRate'],'purchase':exc1['purchaseRate']}}}
        return res
    return "Failed to retrieve data"


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    if len(sys.argv) != 2:
        print("Має бути 2 параметра: назва скрипта і період, за який надати курс валют!")
        quit()

    try:
        t = int(sys.argv[1])
    except ValueError:
        print('Другим парамеиром має бути число від 1 до 10')
        quit()
    if int(t)<1 or int(t)>10:
        print(f'Введено некорректний період у {t} днів! Другим парамеиром має бути число від 1 до 10')
        quit()
    d = datetime.now()
    general_result = []
    for tdate in range(int(t)):
        day = d - timedelta(days=tdate)
        date = day.strftime("%d.%m.%G")
        # print(date)
        result = asyncio.run(get_exchange(date))
        general_result.append(result)
    print(general_result)