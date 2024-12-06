from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot_i import admins, banned

def start_kb(user_telegram_id: int):
    kb_list = []
    for i in range(1, 11, 2):
        t1 = 'Команда ' + str(i)
        t2 = 'Команда ' + str(i+1)
        callback1 = 'show_team_'+ str(i)
        callback2 = 'show_team_'+ str(i+1)
        kb_list.append([InlineKeyboardButton(text=t1, callback_data=callback1), InlineKeyboardButton(text=t2, callback_data=callback2)])
    if user_telegram_id in admins:
        kb_list.append([InlineKeyboardButton(text="⚙️ Админ панель", callback_data='Admin')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
    
def team_kb(user_telegram_id: int, team_id: int):
    kb_list = []
    if user_telegram_id in banned or is_team_full(team_id):
        kb_list.append([InlineKeyboardButton(text="Вернуться назад", callback_data='Home')])
        keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
        return keyboard
    if user_in_team(user_telegram_id, team_id):
        callback_friend = 'Friend_' + str(user_telegram_id)
        kb_list.append([InlineKeyboardButton(text="Придержать место для друга", callback_data=callback_friend)])
    else:
        callback_self = 'Self_' + str(user_telegram_id)
        kb_list.append([InlineKeyboardButton(text="Присоедениться самому", callback_data=callback_self)])
    
    kb_list.append([InlineKeyboardButton(text="Вернуться назад", callback_data='Home')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def admin_kb():
    kb_list = []
    kb_list.append([InlineKeyboardButton(text="Какой-то функционал ¯\_(ツ)_/¯", callback_data='Adminsmth')])
    kb_list.append([InlineKeyboardButton(text="Вернуться назад", callback_data='Home')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
