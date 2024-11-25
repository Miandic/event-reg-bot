from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards import *

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет!\n\nВыбирай команду, к какое хочешь присоедениться и вперёд!\nПосмотреть состав команды можно, нажав на неё. С друзьями веселее!', reply_markup=start_kb(message.from_user.id))


@start_router.callback_query(F.data == 'Home')
async def cmd_start(call: CallbackQuery):
    await call.message.edit_text('Привет!\n\nВыбирай команду, к какое хочешь присоедениться и вперёд!\nПосмотреть состав команды можно, нажав на неё. С друзьями веселее!', reply_markup=start_kb(call.from_user.id))


@start_router.callback_query(F.data.startswith('show_team_'))
async def show_team(call: CallbackQuery):
    team_id = int(call.data.replace('show_team_', ''))
    formatted_message = 'Места:\n\nЗанято: 0\nСвободно:9\nНа удержании:1'

    await call.message.edit_text(formatted_message, reply_markup=team_kb(call.from_user.id, team_id))


@start_router.callback_query(F.data == 'Admin')
async def admin(call: CallbackQuery):
    await call.message.edit_text('Я получил власть, которая и не снилась моему отцу!', reply_markup=admin_kb())