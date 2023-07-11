import asyncio

import aiohttp
from aiogram import Bot, types, Dispatcher
import yaml
import keyboard as kb
import logging
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import sqlite3
import aiosqlite

with open('config.yml') as fh:
    dictionary_data = yaml.safe_load(fh)
TOKEN = dictionary_data['TOKEN']
URL_SHEDULE = dictionary_data['URL_SHEDULE']
PROXY = dictionary_data['PROXY']

logging.basicConfig(level=logging.INFO)

days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
# main_shedule = pd.DataFrame()

bot = Bot(token=TOKEN, proxy=PROXY)
dp = Dispatcher(bot)


async def create_table():
    async with aiosqlite.connect('School124.db') as db:
        await db.execute('CREATE TABLE IF NOT EXISTS users (id text UNIQUE, name text, klass text)')
        await db.commit()


async def get_main_shedule():
    # Парсим основное расписание с сайта
    async with aiohttp.ClientSession() as session:
        # делаем GET-запрос
        testproxy=""
        async with session.get(URL_SHEDULE, proxy=testproxy) as response:  # расписание
            # создаем переменную с ответом сервера
            soup = BeautifulSoup(await response.text(), "lxml")
            head = soup.find("tr")
            headers = ["День недели", "Урок"]
            for i in head.find_all("td")[2:]:
                headers.append(i.text.split('\n')[0])
            global main_shedule
            main_shedule = pd.DataFrame(columns=headers)
            # Create a for loop to fill mydata
            for j in soup.find_all("tr")[1:]:
                row_data = j.find_all("td")
                row = [i.text for i in row_data]
                if len(row) < len(headers):
                    row.insert(0, main_shedule.loc[len(main_shedule) - 1, "День недели"])
                    if row[1] == "\xa0":
                        row[1] = row[13]
                        row[13] = "\xa0"
                elif row[1] == "\xa0":
                    row[0] = row[12]
                    row[12] = "\xa0"
                    row[1] = row[13]
                    row[13] = "\xa0"
                main_shedule.loc[len(main_shedule)] = row
            main_shedule.to_sql("main_shedule", con=sqlite3.connect("School124.db"), if_exists='replace')
            main_shedule.set_index("День недели", inplace=True)
        # return main_shedule


async def registr_user_db(user_id, user, klass):
    # Запись в базу данных ID, имя пользователя и выбранный класс
    async with aiosqlite.connect('School124.db') as db:
        await db.execute('INSERT INTO users VALUES (?, ?, ?) ON CONFLICT(id)'
                         'DO UPDATE SET klass=?', (user_id, user, klass, klass))
        await db.commit()


async def find_user_db(user_id):
    # Поиск класса у зарегистрированного пользователя
    async with aiosqlite.connect('School124.db') as db:
        cursor = await db.execute('SELECT klass FROM users WHERE id = '+str(user_id))
        row = await cursor.fetchone()
        if row is None:
            klass = "None"
        else:
            klass = row[0]
        return klass


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
    await bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! {code}')


@dp.callback_query_handler(lambda c: c.data and c.data.startswith(('5', '6', '7', '8', '9', '10', '11')))
async def process_callback_kb_klass(callback_query: types.CallbackQuery):
    await registr_user_db(callback_query.from_user.id, callback_query.from_user.first_name, callback_query.data)
    await bot.answer_callback_query(callback_query.id, text=f'Выбран класс {callback_query.data}')  # , show_alert=True)
    await bot.send_message(
        callback_query.from_user.id, f'Теперь доступно расписание для класса {callback_query.data} по команде /shedule')


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("Выбери класс, у которого будем отслеживать расписание 🗓!", reply_markup=kb.inline_kb_klass)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Для отслеживания расписания нужно выбрать класс /start и запросить расписание /shedule")


@dp.message_handler(commands=['1'])
async def process_command_1(message: types.Message):
    await message.reply("Первая инлайн кнопка", reply_markup=kb.inline_kb1)


@dp.message_handler(commands=['All'])
async def process_command_2(message: types.Message):
    await message.reply("Отправляю все возможные кнопки", reply_markup=kb.inline_kb_full)


@dp.message_handler(commands=['shedule'])
async def raspis_from_main_shedule(message: types.Message):
    # узнаем какой класс нужно выбрать
    user_klass = await find_user_db(message.from_user.id)
    if user_klass == "None":
        await message.answer("Вначале нужно выбрать класс командой /start")
    else:
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

        df_today = main_shedule.loc[[day1], ["Урок", user_klass]]
        df_tomorrov = main_shedule.loc[[day2], ["Урок", user_klass]]
        str_today = day1 + "\n" + df_today.to_string(index=False) + "\n\n" + day2 + "\n" + df_tomorrov.to_string(
            index=False)
        await message.answer(str_today)


@dp.message_handler()
async def echo_message(msg: types.Message):
    # await bot.send_message(msg.from_user.id, msg.text)
    await msg.reply("Для отслеживания расписания нужно выбрать класс /start и запросить расписание /shedule")


async def main():
    await create_table()
    await get_main_shedule()
    await dp.start_polling(bot)
    # executor.start_polling(dp)


if __name__ == "__main__":
    asyncio.run(main())
