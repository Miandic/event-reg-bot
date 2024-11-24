import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config


admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]
banned = [int(banned_id) for banned_id in config('BLACKLIST').split(',')]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

def is_team_full(team_id):
    status = False
    #Request database and count team members
    return status

def user_in_team(user_id, team_id):
    status = False
    #Request database and check team members
    return status