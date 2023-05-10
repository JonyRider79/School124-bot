import asyncio

import aiohttp
from aiogram import Bot, types, Dispatcher, executor
import yaml
import keyboard as kb
import logging
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import sqlite3


with open('config.yml') as fh:
    dictionary_data = yaml.safe_load(fh)
TOKEN = dictionary_data['TOKEN']

logging.basicConfig(level=logging.INFO)

days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
#main_shedule = pd.DataFrame()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def get_main_shedule():
    # Парсим основное расписание с сайта
    async with aiohttp.ClientSession() as session:
        # делаем GET-запрос
        async with session.get("http://74207s124.edusite.ru/m147731.xml?ver=29254") as response:  # расписание
            # создаем переменную с ответом сервера
            soup = BeautifulSoup(await response.text(), "lxml")
            head = soup.find("tr")
            headers = ["День недели", "Урок"]
            for i in head.find_all("td")[2:]:
                headers.append(i.text)
            global main_shedule
            main_shedule = pd.DataFrame(columns=headers)
            # Create a for loop to fill mydata
            for j in soup.find_all("tr")[1:]:
                row_data = j.find_all("td")
                row = [i.text for i in row_data]
                if len(row) < len(headers):
                    row.insert(0, main_shedule.loc[len(main_shedule)-1,"День недели"])
                    if (row[1]=="\xa0"):
                        row[1] = row[13]
                        row[13] = "\xa0"
                elif (row[1]=="\xa0"):
                    row[0] = row[12]
                    row[12] = "\xa0"
                    row[1] = row[13]
                    row[13] = "\xa0"
                main_shedule.loc[len(main_shedule)] = row
            main_shedule.to_sql("main_shedule", con=sqlite3.connect("School124.db"), if_exists='replace')
            main_shedule.set_index("День недели", inplace=True)
           # return main_shedule



@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 2:
        await bot.answer_callback_query(callback_query.id, text='Нажата вторая кнопка')
    elif code == 5:
        await bot.answer_callback_query(
            callback_query.id,
            text='Нажата кнопка с номером 5.\nА этот текст может быть длиной до 200 символов 😉', show_alert=True)
    else:
        await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! code={code}')



@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!", reply_markup=kb.greet_kb1)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отправлю этот текст тебе в ответ!")

@dp.message_handler(commands=['1'])
async def process_command_1(message: types.Message):
    await message.reply("Первая инлайн кнопка", reply_markup=kb.inline_kb1)


@dp.message_handler(commands=['All'])
async def process_command_2(message: types.Message):
    await message.reply("Отправляю все возможные кнопки", reply_markup=kb.inline_kb_full)

@dp.message_handler(commands=['raspis'])
async def raspis_from_main_shedule(message: types.Message):
    # Узнаем текущий день недели и выводим расписание на два рабочих дня
    my_date = date.today()
    if date.weekday(my_date) == 5:
        day1 = days[5]
        day2 = days[0]
    elif date.weekday(my_date) == 6:
        day1 = days[0]
        day2 = days[1]
    else:
        day1 = days[date.weekday(my_date)]
        day2 = days[date.weekday(my_date) + 1]

    df_today = main_shedule.loc[[day1], ["Урок", '6б']]
    df_tomorrov = main_shedule.loc[[day2], ["Урок", '6б']]
    str_today = day1 + "\n" + df_today.to_string(index=False) + "\n\n" + day2 + "\n" + df_tomorrov.to_string(
        index=False)
    await message.answer(str_today)


@dp.message_handler()
async def echo_message(msg: types.Message):
    #await bot.send_message(msg.from_user.id, msg.text)
    await msg.answer(msg.text)



async def main():
    await get_main_shedule()
    await dp.start_polling(bot)
    #executor.start_polling(dp)


if __name__ == "__main__":
    asyncio.run(main())



