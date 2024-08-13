from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

knb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🪨 Камень", callback_data="rock"), InlineKeyboardButton(text="✂️ Ножницы", callback_data="nozh"), InlineKeyboardButton(text="🧻 Бумага", callback_data="paper")]
])

games = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="1⃣ Угадай число", callback_data="chislo")],
    [InlineKeyboardButton(text="💬 Угадай слово", callback_data="slovo")],
    [InlineKeyboardButton(text="🧻 КНБ", callback_data="knb")],
    [InlineKeyboardButton(text="❌ Назад", callback_data="nazad")]
])

nazad = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="❌ Назад", callback_data="ret")]
])