import random
import os
import sqlite3
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from secret import TOKEN
from create_db import create_locations_db, create_mobs_db, create_person_db, create_items_db, create_items_links_db
import utils

create_locations_db()
create_mobs_db()
create_person_db()
create_items_db()
create_items_links_db()

connect_locations = sqlite3.connect('dbs/locations.db', check_same_thread=False)
cursor_locations = connect_locations.cursor()
connect_mobs = sqlite3.connect('dbs/mobs.db', check_same_thread=False)
cursor_mobs = connect_mobs.cursor()
connect_person = sqlite3.connect('dbs/person.db', check_same_thread=False)
cursor_person = connect_person.cursor()
connect_items = sqlite3.connect('dbs/items.db', check_same_thread=False)
cursor_items = connect_items.cursor()
connect_items_links = sqlite3.connect('dbs/items_links.db', check_same_thread=False)
cursor_items_links = connect_items_links.cursor()

cursor_locations.execute('INSERT INTO locations (LocationName) VALUES (?)', ['center'])
connect_locations.commit()
cursor_locations.execute('INSERT INTO locations (LocationName, XCoord, YCoord) VALUES (?, ?, ?)', ['Novigrad', 0, 2])
connect_locations.commit()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["help"])
async def start(message: types.Message):
    await message.answer(text=utils.HELPER_TEXT)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    cursor_person.execute('INSERT INTO person (ChatId, Nickname) VALUES (?, ?)',
                          [message.chat.id, message.from_user.username])
    connect_person.commit()
    await message.answer(text=utils.HELLO_TEXT)


@dp.message_handler(commands=["stats_player"])
async def start(message: types.Message):
    cursor_person.execute(f"select Nickname, LEVEL, HP, CurHP, Money, Attack, MagicAttack, XP, Armour, MagicArmour, "
                          f"LocationID from person where ChatId = {message.chat.id}")
    person_info = list(cursor_person.fetchall()[0])
    cursor_locations.execute(f'select LocationName, LocationType from locations where LocationID = {person_info[10]}')
    location_info = list(cursor_locations.fetchall()[0])
    await message.answer(text=utils.create_stats_player_text(person_info, location_info))


@dp.message_handler(commands=["stats_cities"])
async def start(message: types.Message):
    cursor_locations.execute(f'select LocationName, LocationType, XCoord, YCoord from locations')
    locations = list(cursor_locations.fetchall())
    await message.answer(text=utils.create_stats_location_text(locations))


@dp.message_handler()
async def unknown_message(message: types.Message):
    """Ответ на любое неожидаемое сообщение"""
    await message.answer(text=utils.UNKNOWN_TEST)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())