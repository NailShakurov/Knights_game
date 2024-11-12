import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = '7886760486:AAGxkEkApKcxksz1cqOaEUivvHrXzb8dNW4'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Game(StatesGroup):
    waiting_for_start = State()
    waiting_for_guess = State()
    waiting_for_restart = State()

# Код самой игры
class GameLogic:
    def __init__(self):
        self.weapon = None
        self.armor = None
        self.transport = None
        self.path = None
        self.dragon_health = 100
        self.alive = True

    def choose_weapon(self):
        return "Выберите оружие:\n1. Меч\n2. Палка\n3. Пулемет"

    def choose_armor(self):
        return "Выберите броню:\n1. Полный латный доспех\n2. Костюм-тройка\n3. Дырявые трусы и носки"

    def choose_transport(self):
        return "Выберите транспорт:\n1. Ковер-самолет\n2. Ослик Иа\n3. Пешком"

    def choose_path(self):
        descriptions = {
            "1": "Вы уперлись в скалы.",
            "2": "Вы увязли в болоте.",
            "4": "Вы вернулись назад и потеряли много времени.",
            "5": "Вы запутались в кустах."
        }
        return "Выберите направление:\n1. Направо\n2. Налево\n3. Прямо\n4. Назад\n5. По диагонали"

    def fight_dragon(self):
        return "В бой с драконом!"

    def reset_game(self):
        self.weapon = None
        self.armor = None
        self.transport = None
        self.path = None
        self.dragon_health = 100
        self.alive = True

# Команды бота
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton('Старт')
    cancel_button = types.KeyboardButton('Отмена')
    markup.add(start_button, cancel_button)
    
    await message.answer("Привет! Добро пожаловать в игру. Чтобы начать, нажми 'Старт'. Чтобы выйти, нажми 'Отмена'.", reply_markup=markup)
    await Game.waiting_for_start.set()

@dp.message_handler(lambda message: message.text == 'Старт', state=Game.waiting_for_start)
async def game_start(message: types.Message, state: FSMContext):
    await message.answer("Игра начинается! Давайте выберем ваше оружие. " + game.choose_weapon())
    await Game.waiting_for_guess.set()

@dp.message_handler(lambda message: message.text == 'Отмена', state=Game.waiting_for_start)
async def cancel_game(message: types.Message, state: FSMContext):
    await message.answer("Игра отменена.")
    await state.finish()

# Обработчики для выбора оружия, брони, транспорта и пути
@dp.message_handler(lambda message: message.text in ['1', '2', '3'], state=Game.waiting_for_guess)
async def process_guess(message: types.Message, state: FSMContext):
    game = GameLogic()
    choice = message.text
    if choice == '1':
        game.weapon = "Меч"
    elif choice == '2':
        game.weapon = "Палка"
    elif choice == '3':
        game.weapon = "Пулемет"
    
    await message.answer(game.choose_armor())
    await Game.waiting_for_guess.set()

# После выбора брони
@dp.message_handler(lambda message: message.text in ['1', '2', '3'], state=Game.waiting_for_guess)
async def process_armor(message: types.Message, state: FSMContext):
    game = GameLogic()
    choice = message.text
    if choice == '1':
        game.armor = "Полный латный доспех"
    elif choice == '2':
        game.armor = "Костюм-тройка"
    elif choice == '3':
        game.armor = "Дырявые трусы и носки"
    
    await message.answer(game.choose_transport())
    await Game.waiting_for_guess.set()

# После выбора транспорта
@dp.message_handler(lambda message: message.text in ['1', '2', '3'], state=Game.waiting_for_guess)
async def process_transport(message: types.Message, state: FSMContext):
    game = GameLogic()
    choice = message.text
    if choice == '1':
        game.transport = "Ковер-самолет"
    elif choice == '2':
        game.transport = "Ослик Иа"
    elif choice == '3':
        game.transport = "Пешком"
    
    await message.answer(game.choose_path())
    await Game.waiting_for_guess.set()

# После выбора пути
@dp.message_handler(lambda message: message.text in ['1', '2', '3', '4', '5'], state=Game.waiting_for_guess)
async def process_path(message: types.Message, state: FSMContext):
    game = GameLogic()
    choice = message.text
    game.path = "Прямо"
    await message.answer(game.fight_dragon())
    await Game.waiting_for_restart.set()

# Завершение игры
@dp.message_handler(lambda message: message.text in ['Да', 'Нет'], state=Game.waiting_for_restart)
async def process_restart(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        game.reset_game()
        await message.answer("Игра начинается заново!")
        await cmd_start(message)
    else:
        await message.answer("Спасибо за игру!")
        await state.finish()

# Обработчик для окончания игры
@dp.message_handler(state=Game.waiting_for_restart)
async def end_game(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes_button = types.KeyboardButton('Да')
    no_button = types.KeyboardButton('Нет')
    markup.add(yes_button, no_button)

    await message.answer("Игра окончена. Хотите сыграть снова?", reply_markup=markup)
    await Game.waiting_for_restart.set()

if __name__ == '__main__':
    game = GameLogic()
    executor.start_polling(dp, skip_updates=True)
