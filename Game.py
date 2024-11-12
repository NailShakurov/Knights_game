@dp.message_handler(commands='start')
async def start_game(message: types.Message):
    game.reset_game()
    await message.reply("Добро пожаловать в игру 'Рыцарь спасает принцессу от дракона'! Введите номер, чтобы выбрать оружие:\n1. Меч\n2. Палка\n3. Пулемет")
    await GameStates.choosing_weapon.set()

@dp.message_handler(state=GameStates.choosing_weapon)
async def choose_weapon(message: types.Message, state: FSMContext):
    choice = message.text
    if choice == "1":
        game.weapon = "Меч"
    elif choice == "2":
        game.weapon = "Палка"
    elif choice == "3":
        game.weapon = "Пулемет"
    else:
        await message.reply("Неправильный выбор. Пожалуйста, введите номер, чтобы выбрать оружие:\n1. Меч\n2. Палка\n3. Пулемет")
        return

    await message.reply(f"Вы выбрали: {game.weapon}. Теперь введите номер, чтобы выбрать броню:\n1. Полный латный доспех\n2. Костюм-тройка\n3. Дырявые трусы и носки")
    await GameStates.choosing_armor.set()

@dp.message_handler(state=GameStates.choosing_armor)
async def choose_armor(message: types.Message, state: FSMContext):
    choice = message.text
    if choice == "1":
        game.armor = "Полный латный доспех"
    elif choice == "2":
        game.armor = "Костюм-тройка"
    elif choice == "3":
        game.armor = "Дырявые трусы и носки"
    else:
        await message.reply("Неправильный выбор. Пожалуйста, введите номер, чтобы выбрать броню:\n1. Полный латный доспех\n2. Костюм-тройка\n3. Дырявые трусы и носки")
        return

    await message.reply(f"Вы выбрали: {game.armor}. Теперь введите номер, чтобы выбрать транспорт:\n1. Ковер-самолет\n2. Ослик Иа\n3. Пешком")
    await GameStates.choosing_transport.set()

@dp.message_handler(state=GameStates.choosing_transport)
async def choose_transport(message: types.Message, state: FSMContext):
    choice = message.text
    if choice == "1":
        game.transport = "Ковер-самолет"
    elif choice == "2":
        game.transport = "Ослик Иа"
    elif choice == "3":
        game.transport = "Пешком"
    else:
        await message.reply("Неправильный выбор. Пожалуйста, введите номер, чтобы выбрать транспорт:\n1. Ковер-самолет\n2. Ослик Иа\n3. Пешком")
        return

    await message.reply(f"Вы выбрали: {game.transport}. Теперь отправляемся в путь! Введите номер для выбора пути.")
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
    await message.reply("Хотите сыграть снова? Введите 'да' или 'нет'.")

@dp.message_handler(lambda message: message.text.lower() == "да", state=GameStates.end_game)
async def restart_game(message: types.Message, state: FSMContext):
    await start_game(message)

@dp.message_handler(lambda message: message.text.lower() == "нет", state=GameStates.end_game)
async def stop_game(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Спасибо за игру!")
