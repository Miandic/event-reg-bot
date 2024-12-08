from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards import *
from sqlalchemy import Integer, String, Boolean, DateTime
from bot_i import bot, dp, admins, banned, pg_manager

router_handler = Router()


start_text = 'Привет!\nЭто бот для регистрации на новогодний квест 11 общежития'

ban_text = 'Ты в бане! По вопросам разбана пиши администратору :p'


async def create_table(table_name='users_ny'):
    async with pg_manager:
        columns = [
            {"name": "id", "type": Integer, "options": {"primary_key": True, "autoincrement": True}},
            {"name": "team_id", "type": Integer},
            {"name": "name", "type": String},
            {"name": "username", "type": String},
            {"name": "status", "type": String},
            {"name": "date", "type": String}]
        await pg_manager.create_table(table_name=table_name, columns=columns)


async def insert_table_team_member(team: int, username: str, reserve: int, table_name='members_ny') -> int:
    async with pg_manager:
        data = await pg_manager.select_data(table_name, where_dict={'username': username})
        for i in data:
            if reserve == 0 and i.get('username') == username:
                return 0
        #data = await pg_manager.select_data(table_name)
        user_info = []
        if reserve > 3:
            return 1
        if reserve > 0:
            for i in range(reserve):
                user_info[i].append({'team': team, 'username': 'Booked', 'booked_by': username})
        else:
            user_info[i].append({'team': team, 'username': username, 'booked_by': 'None'})

        await pg_manager.insert_data_with_update(table_name=table_name, records_data=user_info, conflict_column='id', update_on_conflict=True)


async def get_table_team(team: int, table_name='members_ny'):
    async with pg_manager:
        data = await pg_manager.select_data(table_name, where_dict={'team': team})
        return data
    
    
async def is_team_full(team_id):
    team = get_table_team(team_id)
    total = 0
    for member in team:
        total += 1
    if total < 8:   
        return False
    return True


async def user_in_team(username, team_id):
    team = get_table_team(team_id)
    for member in team:
        if member.get('username') == username:
            return True
    return False


@router_handler.message(CommandStart())
async def cmd_start(message: Message):
    ans = start_text
    if message.from_user.id in banned:
        await message.answer(ban_text, reply_markup=None)
    
    if user_in_team(message.from_user.id, 0):
        ans += 'Ты уже в команде'
    await message.answer(ans, reply_markup=start_kb(message.from_user.id, 10))


@router_handler.callback_query(F.data == 'Home')
async def cmd_start(call: CallbackQuery):
    if call.from_user.id in banned:
        await call.message.edit_text(ban_text, reply_markup=None)

    await call.message.edit_text(start_text, reply_markup=start_kb(call.from_user.id, 10))


@router_handler.callback_query(F.data.startswith('show_team_'))
async def show_team(call: CallbackQuery):
    team_id = int(call.data.replace('show_team_', ''))
    team = get_table_team(team_id)
    occ = 0
    hold = 0
    for member in team:
        if member.get('booked_by') == 'None':
            occ += 1
        else:
            hold += 1

    formatted_message = 'Места: 8\n\nЗанято: ' + str(occ) + '\nНа удержании: ' + str(hold)
    
    await call.message.edit_text(formatted_message, reply_markup=team_kb(call.from_user.id, team_id))


@router_handler.callback_query(F.data == 'Admin')
async def admin(call: CallbackQuery):
    #await create_table()
    await call.message.edit_text('Я получил власть, которая и не снилась моему отцу!', reply_markup=admin_kb())
