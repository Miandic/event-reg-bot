from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot_i import admins, banned

def start_kb(user_telegram_id: int, teams: int):
    kb_list = []
    i = 0
    while i < teams:
        if i + 1 < teams:
            #result = f"{str} {19 + (i - 1) // 4}:{(i - 1) % 4 * 15:02}"
            t1 = f'Команда {str(i+1)} || Старт {19 + (i) // 4}:{(i) % 4 * 15:02}'
            t2 = f'Команда {str(i+2)} || Старт {19 + (i + 1) // 4}:{(i + 1) % 4 * 15:02}'
            callback1 = 'show_team_'+ str(i+1)
            callback2 = 'show_team_'+ str(i+2)
            kb_list.append([InlineKeyboardButton(text=t1, callback_data=callback1), InlineKeyboardButton(text=t2, callback_data=callback2)])
        else:
            kb_list.append([InlineKeyboardButton(text=(f'Команда {str(i+1)} || Старт {19 + (i) // 4}:{(i) % 4 * 15:02}'), callback_data=('show_team_'+ str(i+1)))])
        i += 2
    if user_telegram_id in admins:
        kb_list.append([InlineKeyboardButton(text="⚙️ Админ панель", callback_data='Admin')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
    

def team_kb(user_telegram_id: int, team_id: int):
    kb_list = []
    if user_telegram_id in banned:
        kb_list.append([InlineKeyboardButton(text="Вернуться назад", callback_data='Home')])
        keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
        return keyboard
    else:
        callback_self = f'Self_{str(team_id)}_{str(user_telegram_id)}'
        kb_list.append([InlineKeyboardButton(text="Присоедениться", callback_data=callback_self)])
    
    kb_list.append([InlineKeyboardButton(text="Вернуться назад", callback_data='Home')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def home_kb():
    return InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text="Вернуться назад", callback_data='Home')]])


def is_valid_kb():
    kb_list = [
        [InlineKeyboardButton(text="✅Все верно", callback_data='correct'), InlineKeyboardButton(text="❌Заново", callback_data='incorrect')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def admin_kb():
    kb_list = []
    kb_list.append([InlineKeyboardButton(text="Какой-то функционал ¯\_(ツ)_/¯", callback_data='Adminsmth')])
    kb_list.append([InlineKeyboardButton(text="Вернуться назад", callback_data='Home')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
