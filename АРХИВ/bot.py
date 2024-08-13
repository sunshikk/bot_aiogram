import asyncio  
import logging  
import sys  
from aiogram import Bot, Dispatcher, Router, types 
from aiogram.client.default import DefaultBotProperties  
from aiogram.enums import ParseMode  
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup 

TOKEN = "5929893842:AAHv_f3hyotqkicd8os2hbrwY8akX55JDzU"

router = Router() 
dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

user_data = {
    'fullname': None,
    'username': None,
    'userid': 0,
    'isreg': 0,
    'money': 0
}

@router.message(CommandStart()) 
async def start_command(message: types.Message):
    keyboard = None
    user_data['fullname'] = message.from_user.full_name
    user_data['username'] = message.from_user.username
    user_data['userid'] = message.from_user.id
    if user_data['isreg'] == 1:
        keyboard = InlineKeyboardMarkup( 
        inline_keyboard=[ 
            [InlineKeyboardButton(text="💰 Заработок", callback_data='zarabotok')],
            [InlineKeyboardButton(text="❓ Помощь", callback_data='help')]
        ] 
    )
        text = f"👋 Привет, {user_data['fullname']}!\n✅ Вы успешно авторизовались в боте.\n\nВся необходимая информация есть в: ❓ Помощь"
    else:
        keyboard = InlineKeyboardMarkup( 
        inline_keyboard=[ 
            [InlineKeyboardButton(text="🔰 Зарегистрироваться в боте", callback_data='reginbot')]
        ] 
    )
        text = f"👋 Привет!\nВы не зарегистрированы в боте\n\nДля того, чтобы зарегистрироваться и продолжить, нажмите: '🔰 Зарегистрироваться в боте'"
    
    await message.answer(text, reply_markup=keyboard)


@router.callback_query() 
async def process_callback(callback_query: types.CallbackQuery): 
    data = callback_query.data 
    if data == 'help': 
        await callback_query.answer()
        await callback_query.message.answer(
            "❓ За что отвечают кнопки?:\n\n1. Кнопка '💰 Заработок' отвечает за открытие вкладки для заработка монет\n\n💸 Как заработать денег?:\n\nСпособов заработать денег - несколько:\n1. Заработать денег в кликере (для этого вам нужно перейти во вкладку 💰 Заработок и просто тыкать на кнопку.)",
            reply_markup=types.ReplyKeyboardRemove()
        )
    if data == 'reginbot': 
        await callback_query.answer()
        await callback_query.message.answer(
            "✅ Вы успешно зарегистрированы в боте\nДля продолжения, введите '/start'.",
            reply_markup=types.ReplyKeyboardRemove()
        )
        user_data['isreg'] = 1
    if data == 'zarabotok': 
        await callback_query.answer()
        await callback_query.message.answer(
            "✅ Вы успешно зарегистрированы в боте\nДля продолжения, введите '/start'.",
            reply_markup=types.ReplyKeyboardRemove()
        )

dp.include_router(router) 

async def main() -> None: 
    await dp.start_polling(bot)

if __name__ == "__main__": 
    logging.basicConfig(level=logging.INFO, stream=sys.stdout) 
    asyncio.run(main())