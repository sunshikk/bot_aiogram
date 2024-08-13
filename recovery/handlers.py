import random

from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import files.keyboards as kb
from files import database as db


bot_choice = None

words = [
    "яблоко", "банан", "вишня", "финик", "инжир", "виноград", "киви",
    "лимон", "манго", "нектарин", "апельсин", "папайя", "айва",
    "малина", "клубника", "мандарин", "арбуз", "черника",
    "ежевика", "ананас", "абрикос", "авокадо", "кокос",
    "клюква", "питахайя", "бузина", "грейпфрут", "гуайява",
    "дыня", "джекфрут", "кумкват", "лайм", "личи", "мандарин",
    "шелковица", "маслина", "маракуйя", "персик", "груша", "слива",
    "гранат", "карамбола", "сметанное яблоко", "тамаринд", "угли",
    "киви", "хурма", "крыжовник", "какашка", "город", "страна", "игра",
    "жизнь", "улица", "робот"
]

choices = {"Rock": "Камень", "Nozh": "Ножницы", "Paper": "Бумага"}

class Form(StatesGroup):
    chislo = State()
    slovo = State()

router = Router()

@router.message(StateFilter(None), CommandStart())
async def cmd_start(message: Message):
    keyb = [
        # [kb.KeyboardButton(text="1⃣ Угадай число"), kb.KeyboardButton(text="💬 Угадай слово"), kb.KeyboardButton(text="🧻 Камень Ножницы Бумага")],
        [kb.KeyboardButton(text="🎮 Игры")],
        [kb.KeyboardButton(text="🔑 Статистика")]
    ]
    keyboard = kb.ReplyKeyboardMarkup(keyboard=keyb, resize_keyboard=True)
    user_id = message.from_user.id
    db.cur.execute("INSERT OR IGNORE INTO users (user_id, wins, defeats, draws) VALUES (?, ?, ?, ?)", (user_id, 0, 0, 0))
    db.db.commit()
    await message.answer("👋 Привет!\nВыбери опцию для продолжения", reply_markup=keyboard)


@router.callback_query() 
async def process_callback(callback_query: CallbackQuery, state: FSMContext): 
    data = callback_query.data

    if data == "rock":
        bot_choice = random.choice(["Rock", "Nozh", "Paper"])
        if bot_choice == "Paper":
            await callback_query.bot.edit_message_text(
                text="😔 Вы проиграли!\nБот выбрал: <b>Бумагу</b>!",
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                parse_mode="HTML"
            )
            play = False
            db.cur.execute("UPDATE users SET defeats = defeats + {} WHERE user_id = {}".format(1, callback_query.from_user.id))
            db.db.commit()
        if bot_choice == "Rock":
            await callback_query.bot.edit_message_text(
                text="🫥 Ничья!\nБот выбрал: <b>Камень</b>!",
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                parse_mode="HTML"
            )
            play = False
            db.cur.execute("UPDATE users SET draws = draws + {} WHERE user_id = {}".format(1, callback_query.from_user.id))
            db.db.commit()
        elif bot_choice == "Nozh":
            await callback_query.bot.edit_message_text(
                text="✅ Вы выиграли!\nБот выбрал: <b>Ножницы</b>!",
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                parse_mode="HTML"
            ) 
            play = False
            db.cur.execute("UPDATE users SET wins = wins + {} WHERE user_id = {}".format(1, callback_query.from_user.id))
            db.db.commit()
        keyb = [
            [kb.KeyboardButton(text="🎮 Игры")],
            [kb.KeyboardButton(text="🔑 Статистика")]
        ]
        keyboard = kb.ReplyKeyboardMarkup(keyboard=keyb, resize_keyboard=True)
        await callback_query.message.answer("👋 Поиграем?", reply_markup=keyboard)

    if data == "nozh":
        bot_choice = random.choice(["Rock", "Nozh", "Paper"])
        if bot_choice == "Paper":
            await callback_query.bot.edit_message_text(
                text="✅ Вы выиграли!\nБот выбрал: <b>Бумагу</b>!",
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                parse_mode="HTML"
            )
            db.cur.execute("UPDATE users SET wins = wins + {} WHERE user_id = {}".format(1, callback_query.from_user.id))
            db.db.commit()
            play = False
        if bot_choice == "Rock":
            await callback_query.bot.edit_message_text(
                text="😔 Вы проиграли!\nБот выбрал: <b>Камень</b>!",
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                parse_mode="HTML"
            )
            db.cur.execute("UPDATE users SET defeats = defeats + {} WHERE user_id = {}".format(1, callback_query.from_user.id))
            db.db.commit()
            play = False
        elif bot_choice == "Nozh":
            await callback_query.bot.edit_message_text(
                text="🫥 Ничья!\nБот выбрал: <b>Ножницы</b>!",
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                parse_mode="HTML"
            ) 
            db.cur.execute("UPDATE users SET draws = draws + {} WHERE user_id = {}".format(1, callback_query.from_user.id))
            db.db.commit()
            play = False
        keyb = [
            [kb.KeyboardButton(text="🎮 Игры")],
            [kb.KeyboardButton(text="🔑 Статистика")]
        ]
        keyboard = kb.ReplyKeyboardMarkup(keyboard=keyb, resize_keyboard=True)
        await callback_query.message.answer("👋 Поиграем?", reply_markup=keyboard)

    if data == "paper":
        bot_choice = random.choice(["Rock", "Nozh", "Paper"])
        if bot_choice == "Paper":
            await callback_query.bot.edit_message_text(
                text="🫥 Ничья!\nБот выбрал: <b>Бумагу</b>!",
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                parse_mode="HTML"
            )
            db.cur.execute("UPDATE users SET draws = draws + {} WHERE user_id = {}".format(1, callback_query.from_user.id))
            db.db.commit()
            play = False
        if bot_choice == "Rock":
            await callback_query.bot.edit_message_text(
                text="✅ Вы выиграли!\nБот выбрал: <b>Камень</b>!",
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                parse_mode="HTML"
            )
            db.cur.execute("UPDATE users SET wins = wins + {} WHERE user_id = {}".format(1, callback_query.from_user.id))
            db.db.commit()
            play = False
        elif bot_choice == "Nozh":
            await callback_query.bot.edit_message_text(
                text="😔 Вы проиграли!\nБот выбрал: <b>Ножницы</b>!",
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                parse_mode="HTML"
            ) 
            play = False
            db.cur.execute("UPDATE users SET defeats = defeats + {} WHERE user_id = {}".format(1, callback_query.from_user.id))
            db.db.commit()
        keyb = [
            [kb.KeyboardButton(text="🎮 Игры")],
            [kb.KeyboardButton(text="🔑 Статистика")]
        ]
        keyboard = kb.ReplyKeyboardMarkup(keyboard=keyb, resize_keyboard=True)
        await callback_query.message.answer("👋 Поиграем?", reply_markup=keyboard)
        
    if data == "chislo":
        global numm
        numm = random.randint(1, 100)
        await state.set_state(Form.chislo)
        await callback_query.bot.edit_message_text(
            text="<b>Число загадано!</b>\nВведите число от <b>1 до 100</b>",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            parse_mode="HTML",
            reply_markup=kb.nazad
        )
    
    if data == "slovo":
        global word
        word = random.choice(words)
        first_letter = word[0]
        last_letter = word[-1]
        await state.set_state(Form.slovo)
        await callback_query.bot.edit_message_text(
            text=f"<b>Слово загадано!</b>\nВот подсказка: первая буква <b>'{first_letter}'</b>, последняя буква <b>'{last_letter}'</b>",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            parse_mode="HTML",
            reply_markup=kb.nazad
        )

    if data == "knb":
        await callback_query.bot.edit_message_text(
            text="🎲 Бот выбрал свой ход!\nВаша очередь выбирать: Камень, Ножницы или Бумага",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            parse_mode=None,
            reply_markup=kb.knb
        )

    if data == "nazad":
        keyb = [
            [kb.KeyboardButton(text="🎮 Игры")],
            [kb.KeyboardButton(text="🔑 Статистика")]
        ]
        keyboard = kb.ReplyKeyboardMarkup(keyboard=keyb, resize_keyboard=True)
        await callback_query.bot.delete_message(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            request_timeout=None
        )
        await callback_query.message.answer("👋 Привет!\nВыбери опцию для продолжения", reply_markup=keyboard)

    if data == "ret":
        keyb = [
            [kb.KeyboardButton(text="🎮 Игры")],
            [kb.KeyboardButton(text="🔑 Статистика")]
        ]
        keyboard = kb.ReplyKeyboardMarkup(keyboard=keyb, resize_keyboard=True)
        await callback_query.bot.delete_message(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            request_timeout=None
        )
        await callback_query.message.answer("👋 Привет!\nВыбери опцию для продолжения", reply_markup=keyboard)
        await state.clear() 
        await state.set_state(None) 
        numm = 0


@router.message(StateFilter(None), F.text.lower() == "🔑 статистика") 
async def stata(message: Message):
    defeats = db.cur.execute("SELECT defeats FROM users WHERE user_id = {}".format(message.from_user.id)).fetchone()[0]
    wins = db.cur.execute("SELECT wins FROM users WHERE user_id = {}".format(message.from_user.id)).fetchone()[0]
    draws = db.cur.execute("SELECT draws FROM users WHERE user_id = {}".format(message.from_user.id)).fetchone()[0]

    await message.answer(f"🔑 Ваша статистика:\n\n🏆 Побед - {wins}\n➖ Поражений - {defeats}\n🥉 Ничьих - {draws}\n\n🎯 Общее количество сыгранных игр - {wins + defeats + draws}")


@router.message(Form.chislo) 
async def wait_for_numm(message: Message, state: FSMContext): 
    try: 
        global numm 
        namber = int(message.text) 
        if namber < 1 or namber > 100: 
            await message.answer("Загаданное число от 1 до 100!\nПовторите попытку") 
            return 
        elif namber == numm: 
            await state.clear() 
            await state.set_state(None) 
            numm = 0 
            await message.answer("Поздравляю! Вы <b>отгадали</b> загаданное число", parse_mode="HTML") 
            db.cur.execute("UPDATE users SET wins = wins + {} WHERE user_id = {}".format(1, message.from_user.id)) 
            db.db.commit()
        elif namber < numm: 
            await message.answer("Введенное вами число <b>выше</b>, чем загаданное!\nВведите число снова.", parse_mode="HTML") 
        elif namber > numm: 
            await message.answer("Введенное вами число <b>ниже</b>, чем загаданное!\nВведите число снова.", parse_mode="HTML") 
    except ValueError: 
        await message.reply("Пожалуйста, введите корректное числовое значение:")


@router.message(Form.slovo)
async def wait_for_slovo(message: Message, state: FSMContext):
    first_letter = word[0]
    last_letter = word[-1]
    if message.text.lower() == word:
        await state.clear()
        await state.set_state(None)
        await message.answer("Поздравляю! Вы <b>отгадали</b> загаданное слово", parse_mode="HTML")
        db.cur.execute("UPDATE users SET wins = wins + {} WHERE user_id = {}".format(1, message.from_user.id))
        db.db.commit()
    else:
        await message.answer(f"Неправильное слово!\nПодсказка: <b>загаданное слово начинается на {first_letter} и заканчивается на {last_letter}</b>", parse_mode="HTML")


@router.message(F.text.lower() == "🎮 игры")
async def games(message: Message):
    await message.answer("✅", reply_markup=kb.ReplyKeyboardRemove())
    await message.answer("🎮 Выберите, в какую игру вы желаете поиграть", reply_markup=kb.games)
