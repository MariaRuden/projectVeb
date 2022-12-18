import requests
import datetime
import random
from aiogram import Bot, Dispatcher, executor, types
from config import google_search_token
from config import API_TOKEN
from serpapi import GoogleSearch
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from random import randrange

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())



@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет☆\nЯ твой бот для вдохновения на каждый день\nУ меня есть несколько функций:\n/start\n/list\n/search")
    
class FSMText(StatesGroup):
    search_name = State()

def pict_search(name_picture):
    list_img = []

    params = {
        "engine": "yandex_images",
        "text": name_picture,
        "api_key": google_search_token
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    for i in results["images_results"]:
        list_img.append(i["original"])

    return list_img



@dp.message_handler(commands=['search'])
async def search_answer(message: types.Message):
    if message.text == "/search":
        kb = [
            [
                types.KeyboardButton(text="Food"),
                types.KeyboardButton(text="Look"),
                types.KeyboardButton(text="Flowers"),
                types.KeyboardButton(text="PhotoIdeas")
            ],
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
        )
        await message.answer('Выберите то, чем хотите поинтересоваться сегодня', reply_markup=keyboard)
        await FSMText.search_name.set()
        @dp.message_handler(state=FSMText.search_name)
        async def send_pictures(message: types.Message):
            
            answer = message.text

            glp = pict_search(answer)


            for i in range(2):
                await bot.send_photo(message.chat.id, photo=random.choice(glp))


@dp.message_handler(commands=['list'])
async def list(message: types.Message):
    await message.answer("Команды: \n/start \n/list \n/search")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

