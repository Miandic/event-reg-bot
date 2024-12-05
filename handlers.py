from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards import *
from sqlalchemy import Integer, String, Boolean, TIMESTAMP
from bot_i import bot, admins, pg_manager

start_router = Router()


async def create_table_team(table_name='members_ny'):
    async with pg_manager:
        columns = [
            {"name": "id", "type": Integer, "options": {"primary_key": True, "autoincrement": True}},
            {"name": "team", "type": Integer},
            {"name": "username", "type": String},
            {"name": "booked_by", "type": String},
            {"name": "time", "type": TIMESTAMP}]
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


async def get_table_team_member(team: int, table_name='members_ny'):
    async with pg_manager:
        data = await pg_manager.select_data(table_name, where_dict={'team': team})
        return data
    
    
async def is_team_full(team_id):
    team = get_table_team_member(team_id)
    total = 0
    for member in team:
        total += 1
    if total < 8:
        return False
    return True


async def user_in_team(username, team_id):
    team = get_table_team_member(team_id)
    for member in team:
        if member.get('username') == username:
            return True
    return False


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет!\n\nВыбирай команду, к какое хочешь присоедениться и вперёд!\nПосмотреть состав команды можно, нажав на неё. С друзьями веселее!', reply_markup=start_kb(message.from_user.id))


@start_router.callback_query(F.data == 'Home')
async def cmd_start(call: CallbackQuery):
    await call.message.edit_text('Привет!\n\nВыбирай команду, к какое хочешь присоедениться и вперёд!\nПосмотреть состав команды можно, нажав на неё. С друзьями веселее!', reply_markup=start_kb(call.from_user.id))


@start_router.callback_query(F.data.startswith('show_team_'))
async def show_team(call: CallbackQuery):
    team_id = int(call.data.replace('show_team_', ''))
    team = get_table_team_member(team_id)
    occ = 0
    hold = 0
    for member in team:
        if member.get('booked_by') == 'None':
            occ += 1
        else:
            hold += 1

    formatted_message = 'Места: 8\n\nЗанято: ' + str(occ) + '\nНа удержании: ' + str(hold)
    
    await call.message.edit_text(formatted_message, reply_markup=team_kb(call.from_user.id, team_id))


@start_router.callback_query(F.data == 'Admin')
async def admin(call: CallbackQuery):
    await call.message.edit_text('Я получил власть, которая и не снилась моему отцу!', reply_markup=admin_kb())
