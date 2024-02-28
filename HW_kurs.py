import aiohttp
import asyncio
import platform
from datetime import datetime, timedelta
import sys


async def main(num_date):    
    data1 = []
    try:   
        async with aiohttp.ClientSession() as session:
            for i in range(num_date):
                date_api = date_now - timedelta(i)
                async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date_api.__format__('%d.%m.%Y')}') as response:
                    if response.status == 200:
                        data =  await response.json()
                        data2 = await obrobka(data['exchangeRate'])
                        data1.append({date_api.__format__('%d.%m.%Y'):data2})
                    else:
                        print(f"Error status: {response.status} ")
    
    except ValueError as er:
        print(er)
    except IndexError as er:
        print(er)
    except aiohttp.ClientConnectorError as err:
        print(f'Connection error: {err}')
    
    return data1

async def obrobka(data):
    data2 = {}
    for i in data:
        if i['currency'] in ('EUR', 'USD'):
            data2[i['currency']] = {'sale': i['saleRateNB'], 'purchase': i['purchaseRateNB']}
    return data2
    

if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    date_now = datetime.now().date()
    num_date = int(sys.argv[1])
    if num_date > 10 or num_date < 1:
        print('Обмеження. Значення у межах 1 - 10')
        sys.exit(0)
    
    res = asyncio.run(main(num_date))
    for i in res:
        print(i)
