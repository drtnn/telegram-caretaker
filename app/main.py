import asyncio
import logging
import sys

from app.controller.channel import router as channel_router
from app.controller.private import router as user_router
from app.loader import dp, bot


async def main() -> None:
    dp.include_router(channel_router)
    dp.include_router(user_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
