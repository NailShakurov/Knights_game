import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = 'YOUR_API_TOKEN_HERE'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class GameStates(StatesGroup):
    choosing_weapon = State()
    choosing_armor = State()
    choosing_transport = State()
    choosing_path = State()
    fighting_dragon = State()
    end_game = State()

class GameLogic:
    def __init__(self):
        self.weapon = None
        self.armor = None
        self.transport = None
        self.dragon_health = 100
        self.alive = True

    def reset_game(self):
        self.weapon = None
        self.armor = None
        self.transport = None
        self.dragon_health = 100
        self.alive = True

game = GameLogic()

@dp.message_handler(commands='start')
async def start_game(message: types.Message):
    game.reset_game()
    await message.reply("Добро пожаловать в игру 'Рыцарь спасает принцессу от дракона'! Выберите оружие:", 
                        reply_markup=weapon_keyboard())
    await GameStates.choosing_weapon.set()

def weapon_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("1. Меч", "2. Палка", "3. Пулемет")
    return keyboard

def armor_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("1. Полный латный доспех", "2. Костюм-тройка", "3. Дырявые трусы и носки")
    return keyboard

def transport_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("1. Ковер-самолет", "2. Ослик Иа", "3. Пешком")
    return keyboard

@dp.message_handler(state=GameStates.choosing_weapon)
async def choose_weapon(message: types.Message, state: FSMContext):
    choice = message.text
    if choice == "1. Меч":
        game.weapon = "Меч"
    elif choice == "2. Палка":
        game.weapon = "Палка"
    elif choice == "3. Пулемет":
        game.weapon = "Пулемет"
    else:
        await message.reply("Неправильный выбор. Пожалуйста, выберите оружие снова:", reply_markup=weapon_keyboard())
        return

    await message.reply(f"Вы выбрали: {game.weapon}. Теперь выберите броню:", reply_markup=armor_keyboard())
    await GameStates.choosing_armor.set()

@dp.message_handler(state=GameStates.choosing_armor)
async def choose_armor(message: types.Message, state: FSMContext):
    choice = message.text
    if choice == "1. Полный латный доспех":
        game.armor = "Полный латный доспех"
    elif choice == "2. Костюм-тройка":
        game.armor = "Костюм-тройка"
    elif choice == "3. Дырявые трусы и носки":
        game.armor = "Дырявые трусы и носки"
    else:
        await message.reply("Неправильный выбор. Пожалуйста, выберите броню снова:", reply_markup=armor_keyboard())
        return

    await message.reply(f"Вы выбрали: {game.armor}. Теперь выберите транспорт:", reply_markup=transport_keyboard())
    await GameStates.choosing_transport.set()

@dp.message_handler(state=GameStates.choosing_transport)
async def choose_transport(message: types.Message, state: FSMContext):
    choice = message.text
    if choice == "1. Ковер-самолет":
        game.transport = "Ковер-самолет"
    elif choice == "2. Ослик Иа":
        game.transport = "Ослик Иа"
    elif choice == "3. Пешком":
        game.transport = "Пешком"
    else:
        await message.reply("Неправильный выбор. Пожалуйста, выберите транспорт снова:", reply_markup=transport_keyboard())
        return

    await message.reply(f"Вы выбрали: {game.transport}. Теперь отправляемся в путь!")
    await GameStates.choosing_path.set()

@dp.message_handler(state=GameStates.choosing_path)
async def choose_path(message: types.Message, state: FSMContext):
    descriptions = {
        "1": "Вы уперлись в скалы.",
        "2": "Вы увязли в болоте.",
        "4": "Вы вернулись назад и потеряли много времени.",
        "5": "Вы запутались в кустах."
    }
    correct_direction = str(random.choice([1, 2, 3]))
    choice = message.text

    if choice == correct_direction:
        await message.reply("Вы выбрали верное направление и добрались до замка дракона!")
        await GameStates.fighting_dragon.set()
        await fight_dragon(message)
    else:
        await message.reply(descriptions.get(choice, "Неправильное направление. Попробуйте снова."))

async def fight_dragon(message: types.Message):
    if game.weapon == "Пулемет" and game.armor == "Полный латный доспех":
        await message.reply("Дракон испугался и убежал без боя! Вы выиграли!")
    elif game.weapon == "Палка" and game.armor == "Дырявые трусы и носки":
        await message.reply("Дракон умирает от смеха при виде вашего снаряжения! Вы выиграли!")
    else:
        await message.reply("Вы вступаете в бой с драконом!")
        game.dragon_health -= 50
        if game.dragon_health <= 0:
            await message.reply("Вы победили дракона!")
        else:
            await message.reply("Дракон победил вас.")
    await end_game(message)

async def end_game(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Да", "Нет")
    await message.reply("Хотите сыграть снова?", reply_markup=keyboard)
    await GameStates.end_game.set()

@dp.message_handler(lambda message: message.text.lower() == "да", state=GameStates.end_game)
async def restart_game(message: types.Message, state: FSMContext):
    await start_game(message)

@dp.message_handler(lambda message: message.text.lower() == "нет", state=GameStates.end_game)
async def stop_game(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Спасибо за игру!", reply_markup=types.ReplyKeyboardRemove())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
# 3 version