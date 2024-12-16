from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards import *
from sqlalchemy import Integer, String, Boolean, DateTime
from bot_i import bot, dp, admins, banned, pg_manager
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.chat_action import ChatActionSender
from datetime import datetime

router_handler = Router()

class Form(StatesGroup):
    team = State()
    username = State()
    name = State()
    verify = State()


dbt_name = 'users_ny'
start_text = 'Привет!\nЭто бот для регистрации на новогодний квест 11 общежития'
ban_text = 'Ты в бане! По вопросам разбана пиши администратору :p'


async def create_table(table_name=dbt_name):
    async with pg_manager:
        columns = [
            {"name": "id", "type": Integer, "options": {"primary_key": True, "autoincrement": True}},
            {"name": "team_id", "type": Integer},
            {"name": "name", "type": String},
            {"name": "username", "type": String},
            {"name": "status", "type": String},
            {"name": "date", "type": String}]
        await pg_manager.create_table(table_name=table_name, columns=columns)


async def insert_table_member(team_id: int, name: str, username: str, status: str, date: int, table_name=dbt_name):
    async with pg_manager:
        member_info = {'team_id': team_id, 'name': name, 'username': username, 'status': status, 'date': date}
        await pg_manager.insert_data_with_update(table_name=table_name, records_data=member_info, conflict_column='id', update_on_conflict=True)


async def get_table_members(table_name=dbt_name):
    async with pg_manager:
        data = await pg_manager.select_data(table_name)
        return data


@router_handler.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    msg = start_text
    if message.from_user.id in banned:
        await message.answer(ban_text, reply_markup=None)
        return
    
    data = await get_table_members()
    for i in data:
        if message.from_user.id == i.get('username') or message.from_user.username == i.get('username'):
            msg += '\n\nТы уже в команде. Заходи в чат участников: https://t.me/+zg_wHbf3f5A0YjRi'
            await message.answer(msg, reply_markup=None)
            return

    msg += '\n\nВыбирай команду и присоединяйся'
    await message.answer(msg, reply_markup=start_kb(message.from_user.username, 7))


@router_handler.callback_query(F.data == 'Home')
async def cmd_start(call: CallbackQuery, state: FSMContext):
    await state.clear()
    
    msg = start_text
    if call.message.from_user.id in banned:
        await call.message.edit_text(ban_text, reply_markup=None)
        return

    data = await get_table_members()
    for i in data:
        if call.message.from_user.id == i.get('username') or call.message.from_user.username == i.get('username'):
            msg += '\n\nТы уже в команде. Заходи в чат участников: https://t.me/+zg_wHbf3f5A0YjRi'
            await call.message.edit_text(msg, reply_markup=None)
            return

    msg += '\n\nВыбирай команду и присоединяйся'
    await call.message.edit_text(msg, reply_markup=start_kb(call.message.from_user.id, 7))

    
@router_handler.callback_query(F.data.startswith('show_team_'))
async def show_team(call: CallbackQuery, state: FSMContext):
    await state.set_state(Form.team)

    formatted_message = ''
    
    team_id = int(call.data.replace('show_team_', ''))
    data = await get_table_members()
    occ = 0
    for i in data:
        print(i)
        print(i.get('team_id'))
        print(str(team_id))
        if str(i.get('team_id')) == str(team_id):
            occ += 1
    
    if occ >= 7:
        formatted_message += '❌Команда полная❌'
        await call.message.edit_text(formatted_message, reply_markup=home_kb())
        return
    formatted_message += f'Всего мест: 7 | Из них занято: {str(occ)}'

    await state.update_data(team=team_id)

    await call.message.edit_text(formatted_message, reply_markup=team_kb(call.from_user.username, team_id))


@router_handler.callback_query(F.data.startswith('Self_'))
async def show_team(call: CallbackQuery, state: FSMContext):
    await state.set_state(Form.username)

    team_id = int(call.data.replace('Self_', '')[0])
    user_id = call.data.replace('Self_', '')[2:]

    await state.update_data(username=user_id)

    await call.message.edit_text(f'Чтобы присоедениться к команде №{team_id}, напиши как тебя зовут', reply_markup=home_kb())
    await state.set_state(Form.name)


@router_handler.message(Form.name)
async def get_name(message: Message, state: FSMContext):
    if not message.text:
        await message.answer('Имя нужно писать текстом -_-', reply_markup=home_kb())
        return
    await state.update_data(name=message.text)
    await state.set_state(Form.verify)
    data = await state.get_data()

    reply_text = f'{data.get("name")}, верно?'
    
    await message.answer(reply_text, reply_markup=is_valid_kb())


@router_handler.callback_query(F.data == 'correct', Form.verify)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if call.message.from_user.id in banned:
        await call.message.edit_text('Ты в бане! По вопросам разбана пиши администратору :P', reply_markup=None)
        await state.clear()
        return
    now = datetime.now()
    start_of_month = datetime(now.year, now.month, 1)
    delta = now - start_of_month
    minutes = delta.days * 24 * 60 + delta.seconds // 60
    await insert_table_member(int(data.get('team')), data.get('name'), data.get('username'), 'Ok', str(minutes))
    table = await get_table_members()
    
    for u in table:
        if u.get('username') == data.get('username'):
            idd = u.get('id')
    await call.message.edit_text(f'Спасибо за регистрацию! Твой ID на мероприятии: {idd}\n\nВступай в чат участников, там все подробности! t.me/+zg_wHbf3f5A0YjRi', reply_markup=home_kb())
    await state.clear()


@router_handler.callback_query(F.data == 'incorrect', Form.verify)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await cmd_start(call, state)


@router_handler.callback_query(F.data == 'Admin')
async def admin(call: CallbackQuery):
    #await create_table()
    await call.message.edit_text('Я получил власть, которая и не снилась моему отцу!', reply_markup=admin_kb())
