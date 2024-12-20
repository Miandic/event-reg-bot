import asyncio
from bot_i import bot, dp
from handlers import router_handler


async def main():
    dp.include_router(router_handler)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())