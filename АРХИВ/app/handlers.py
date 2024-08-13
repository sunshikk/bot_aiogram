from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State

import app.keyboards as kb
import app.database.requests as rq
from app.database.models import async_session
from app.database.models import fetch_value

user_data = {
    'UserID': 0,
    'money': 0
}

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_data['UserID'] = message.from_user.id
    await rq.set_user(user_data['UserID'])
    keyb = [
        [kb.KeyboardButton(text="❓ Помощь")],[kb.KeyboardButton(text="💰 Заработок")],
        [kb.KeyboardButton(text="💼 Статистика")]
    ]
    keyboard = kb.ReplyKeyboardMarkup(keyboard=keyb)
    text = f'👋 Привет, {message.from_user.full_name}!\nВы успешно запустили бота и авторизовались\n\n❓ Для получения помощи, нажмите: "❓ Помощь"'
    user_data['UserID'] = await fetch_value('moneyy')
    await message.answer(text, reply_markup=keyboard)

@router.callback_query() 
async def process_callback(callback_query: CallbackQuery): 
    data = callback_query.data

    if data == 'click':
        user_data['money'] += 1
        await callback_query.bot.edit_message_text(
            text=f"💰 Выберите пункт для заработка:\nЕсли вы захотите использовать кликер для заработка, нажмите на '💎 Кликер'\n\nВаш текущий баланс: {user_data['money']} 💰",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            parse_mode=None,
            reply_markup=kb.zarabotok
        )
        await rq.update_user(user_data['UserID'], user_data['money'])

@router.message(F.text.lower() == '❓ помощь')
async def help_button(message: Message):
    await message.reply("❓ За что отвечают кнопки?:\n\n1. Кнопка '💰 Заработок' отвечает за открытие вкладки для заработка монет\n\n💸 Как заработать денег?:\n\nСпособов заработать денег - несколько:\n1. Заработать денег в кликере (для этого вам нужно перейти во вкладку 💰 Заработок и просто тыкать на кнопку.)")

@router.message(F.text.lower() == '💰 заработок')
async def zar_button(message: Message):
    await message.answer(f"💰 Выберите пункт для заработка:\nЕсли вы захотите использовать кликер для заработка, нажмите на '💎 Кликер'\n\nВаш текущий баланс: {user_data['money']} 💰", reply_markup=kb.zarabotok)