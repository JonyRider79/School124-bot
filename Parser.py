'''
Простой асинхронный парсер на Python
Лицензия: MIT
Автор: Марк Фомин
Электронная почта: luring.uliksir@gmail.com
'''
import sqlite3

# импортируем нужные модули
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date

# создаем основную функцию
async def main():
    # создаем асинхронную сессию соединения
    async with aiohttp.ClientSession() as session:
        # делаем GET-запрос
        async with session.get("http://74207s124.edusite.ru/m147731.xml?ver=29254") as response:  # расписание
            # "http: // 74207s124.edusite.ru / m65889.xml?ver = 84427" #изменение уроков
            # выводим код этого запроса
            # print("Status:", response.status)
            # выводим content-type
            # print("Content-type:", response.headers['content-type'])
            # создаем переменную с ответом сервера
            soup = BeautifulSoup(await response.text(), "lxml")
            head = soup.find("tr")
            headers = ["День недели", "Урок"]
            for i in head.find_all("td")[2:]:
                headers.append(i.text)
            # Create a dataframe
            mydata = pd.DataFrame(columns=headers)
            # Create a for loop to fill mydata
            for j in soup.find_all("tr")[1:]:
                row_data = j.find_all("td")
                row = [i.text for i in row_data]
                if len(row) < len(headers):
                    row.insert(0, mydata.loc[len(mydata)-1,"День недели"])
                    if (row[1]=="\xa0"):
                        row[1] = row[13]
                        row[13] = "\xa0"
                elif (row[1]=="\xa0"):
                    row[0] = row[12]
                    row[12] = "\xa0"
                    row[1] = row[13]
                    row[13] = "\xa0"
                mydata.loc[len(mydata)] = row
                #print(mydata)
            # mydata.to_csv("raspisanie.csv", index=False)
            # mydata.to_sql("main_shedule", con=sqlite3.connect("School124.db"), if_exists='replace')
            # df_new = mydata[mydata['День недели'] == 'Понедельник']
            # print(df_new)
            # df_new1 = df_new[["Урок",'6б']]
            # print(df_new1)
            days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
            my_date = date.today()
            if date.weekday(my_date) == 5:
                day1 = days[5]
                day2 = days[0]
            elif date.weekday(my_date) == 6:
                day1 = days[0]
                day2 = days[1]
            else:
                day1 = days[date.weekday(my_date)]
                day2 = days[date.weekday(my_date)+1]

            #print(day1, day2)


            mydata.set_index("День недели", inplace=True)
            df_today = mydata.loc[[day1],["Урок",'6б']]
            df_tomorrov = mydata.loc[[day2],["Урок",'6б']]
            # print(df_new3)
            str_today = day1+"\n"+df_today.to_string(index=False)+"\n\n"+day2+"\n"+df_tomorrov.to_string(index=False)

            print(str_today)

            # for tag in soup.find_all("td"):
            #    print(tag.text)
            # print(soup.td.text)



loop = asyncio.get_event_loop()
loop.run_until_complete(main())
