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
class Game:
    def __init__(self):
        self.weapon = None
        self.armor = None
        self.transport = None
        self.path = None
        self.dragon_health = 100
        self.alive = True

    def choose_weapon(self):
        print("Выберите оружие:")
        print("1. Меч")
        print("2. Палка")
        print("3. Пулемет")
        choice = input("Ваш выбор (1/2/3): ")
        if choice == '1':
            self.weapon = "Меч"
        elif choice == '2':
            self.weapon = "Палка"
        elif choice == '3':
            self.weapon = "Пулемет"
        else:
            print("Неправильный выбор. Попробуйте снова.")
            self.choose_weapon()

    def choose_armor(self):
        print("Выберите броню:")
        print("1. Полный латный доспех")
        print("2. Костюм-тройка")
        print("3. Дырявые трусы и носки")
        choice = input("Ваш выбор (1/2/3): ")
        if choice == '1':
            self.armor = "Полный латный доспех"
        elif choice == '2':
            self.armor = "Костюм-тройка"
        elif choice == '3':
            self.armor = "Дырявые трусы и носки"
        else:
            print("Неправильный выбор. Попробуйте снова.")
            self.choose_armor()

    def choose_transport(self):
        print("Выберите транспорт:")
        print("1. Самокат")
        print("2. Осел")
        print("3. Пешком")
        choice = input("Ваш выбор (1/2/3): ")
        if choice == '1':
            self.transport = "Самокат"
        elif choice == '2':
            self.transport = "Осел"
        elif choice == '3':
            self.transport = "Пешком"
        else:
            print("Неправильный выбор. Попробуйте снова.")
            self.choose_transport()

    def choose_path(self):
        descriptions = {
            "1": "Вы уперлись в скалы.",
            "2": "Вы увязли в болоте.",
            "4": "Вы вернулись назад и потеряли много времени.",
            "5": "Вы запутались в кустах."
        }
        print("Выберите направление:")
        for step in range(1, self.get_path_steps() + 1):
            correct_direction = str(random.choice([1, 2, 3, 4, 5]))  # Случайный правильный выбор
            print(f"Шаг {step}:")
            print("1. Направо")
            print("2. Налево")
            print("3. Прямо")
            print("4. Назад")
            print("5. По диагонали")
            choice = input("Ваш выбор (1/2/3/4/5): ")
            if choice == correct_direction:
                print("Вы идете верным путем. Выберите дальнейшее направление.")
            else:
                print(descriptions.get(choice, "Неправильное направление. Попробуйте снова."))
                return self.choose_path()

        self.path = "Прямо"
        print("Вы выбрали правильное направление и добрались до замка дракона!")

    def get_path_steps(self):
        if self.transport == "Пешком":
            return 3
        elif self.transport == "Самокат":
            return 2
        elif self.transport == "Осел":
            return 1
        return 3

    def fight_dragon(self):
        print("В бой с драконом!")
        if self.weapon == "Пулемет" and self.armor == "Полный латный доспех":
            print("Дракон испугался и убежал без боя!")
            self.alive = True
            return
        elif self.weapon == "Палка" and self.armor == "Дырявые трусы и носки":
            print("Дракон, увидев вас в таком наряде, умирает от смеха, и вы спасаете принцессу!")
            self.alive = True
            return
        else:
            for i in range(4):
                print(f"Действие {i+1}:")
                print("1. Атака")
                print("2. Защита")
                print("3. Уворот")
                choice = input("Ваш выбор (1/2/3): ")
                if choice == '1':
                    self.dragon_health -= 25
                    print(f"Вы нанесли урон дракону. Осталось здоровья у дракона: {self.dragon_health}%")
                    if self.dragon_health <= 0:
                        print("Вы победили дракона!")
                        break
                else:
                    self.alive = False
                    print("Вы совершили ошибку и погибли в бою.")
                    break

    def start_game(self):
        print("Добро пожаловать в игру 'Рыцарь спасает принцессу от дракона'!")
        self.choose_weapon()
        self.choose_armor()
        self.choose_transport()
        self.choose_path()
        if self.alive:
            self.fight_dragon()
        if self.alive:
            print("Вы спасли принцессу и вернулись домой героем!")
        else:
            print("Игра окончена. Вы погибли.")
        
        # Добавляем предложение сыграть заново
        play_again = input("Хотите сыграть снова? (да/нет): ").strip().lower()
        if play_again == 'да':
            self.reset_game()
            self.start_game()
        else:
            print("Спасибо за игру!")

    def reset_game(self):
        self.weapon = None
        self.armor = None
        self.transport = None
        self.path = None
        self.dragon_health = 100
        self.alive = True

if __name__ == "__main__":
    game = Game()
    game.start_game()

import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = 'YOUR_API_TOKEN'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Состояния для каждого этапа игры
class GameStates(StatesGroup):
    choose_weapon = State()
    choose_armor = State()
    choose_transport = State()
    choose_path = State()
    fight_dragon = State()

# Инициализация игры
class Game:
    def __init__(self):
        self.weapon = None
        self.armor = None
        self.transport = None
        self.path = None
        self.dragon_health = 100
        self.alive = True

    def reset_game(self):
        self.weapon = None
        self.armor = None
        self.transport = None
        self.path = None
        self.dragon_health = 100
        self.alive = True

game = Game()  # Создаем экземпляр игры

# Старт игры
@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    game.reset_game()
    await message.reply("Добро пожаловать в игру 'Рыцарь спасает принцессу от дракона'! "
                        "Выберите свое оружие: 1. Меч, 2. Палка, 3. Пулемет.")
    await GameStates.choose_weapon.set()

# Выбор оружия
@dp.message_handler(state=GameStates.choose_weapon)
async def choose_weapon(message: types.Message, state: FSMContext):
    choice = message.text
    if choice == '1':
        game.weapon = "Меч"
    elif choice == '2':
        game.weapon = "Палка"
    elif choice == '3':
        game.weapon = "Пулемет"
    else:
        await message.reply("Неправильный выбор. Попробуйте снова: 1. Меч, 2. Палка, 3. Пулемет.")
        return
    await message.reply("Выберите броню: 1. Полный латный доспех, 2. Костюм-тройка, 3. Дырявые трусы и носки.")
    await GameStates.choose_armor.set()

# Выбор брони
@dp.message_handler(state=GameStates.choose_armor)
async def choose_armor(message: types.Message, state: FSMContext):
    choice = message.text
    if choice == '1':
        game.armor = "Полный латный доспех"
    elif choice == '2':
        game.armor = "Костюм-тройка"
    elif choice == '3':
        game.armor = "Дырявые трусы и носки"
    else:
        await message.reply("Неправильный выбор. Попробуйте снова: 1. Полный латный доспех, 2. Костюм-тройка, 3. Дырявые трусы и носки.")
        return
    await message.reply("Выберите транспорт: 1. Самокат, 2. Осел, 3. Пешком.")
    await GameStates.choose_transport.set()

# Выбор транспорта
@dp.message_handler(state=GameStates.choose_transport)
async def choose_transport(message: types.Message, state: FSMContext):
    choice = message.text
    if choice == '1':
        game.transport = "Самокат"
    elif choice == '2':
        game.transport = "Осел"
    elif choice == '3':
        game.transport = "Пешком"
    else:
        await message.reply("Неправильный выбор. Попробуйте снова: 1. Самокат, 2. Осел, 3. Пешком.")
        return
    await message.reply("Выберите направление: 1. Направо, 2. Налево, 3. Прямо, 4. Назад, 5. По диагонали.")
    await GameStates.choose_path.set()

# Выбор пути
@dp.message_handler(state=GameStates.choose_path)
async def choose_path(message: types.Message, state: FSMContext):
    descriptions = {
        "1": "Вы уперлись в скалы.",
        "2": "Вы увязли в болоте.",
        "4": "Вы вернулись назад и потеряли много времени.",
        "5": "Вы запутались в кустах."
    }
    choice = message.text
    correct_direction = str(random.choice([1, 2, 3, 4, 5]))
    if choice == correct_direction:
        await message.reply("Вы идете верным путем и добрались до замка дракона!")
        await GameStates.fight_dragon.set()
        await message.reply("В бой с драконом! Выберите действие: 1. Атака, 2. Защита, 3. Уворот.")
    else:
        await message.reply(descriptions.get(choice, "Неправильное направление. Попробуйте снова."))
        return

# Бой с драконом
@dp.message_handler(state=GameStates.fight_dragon)
async def fight_dragon(message: types.Message, state: FSMContext):
    choice = message.text
    if choice == '1':
        game.dragon_health -= 25
        if game.dragon_health <= 0:
            await message.reply("Вы победили дракона и спасли принцессу!")
            await state.finish()
            return
        else:
            await message.reply(f"Вы нанесли урон дракону. Осталось здоровья у дракона: {game.dragon_health}%")
            await message.reply("Выберите действие: 1. Атака, 2. Защита, 3. Уворот.")
    else:
        await message.reply("Вы совершили ошибку и погибли в бою.")
        await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
