import asyncio
import logging
import sys

from application import bot, dp


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
