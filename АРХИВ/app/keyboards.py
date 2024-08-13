from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

zarabotok = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💎 Кликер', callback_data='click')]
])

reg = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔑 Зарегистрироваться', callback_data='reg')]
])