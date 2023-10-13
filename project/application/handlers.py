import asyncio
import aiofiles
import os

import aiohttp

from application.bot import bot

from aiogram import types, Dispatcher, F
from aiogram.filters import CommandStart

from openai_service.async_agent import Agent
from openai_service.async_chat import Chat

chat = Chat()
agent = Agent()
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer("Hi! I am bot. How can I help you?")


@dp.message(F.text)
async def echo_handler(message: types.Message):
    request_topic = f"To which topic does this text refer: '{message.text}'. Write only the name of the subject"
    response_topic = (await chat.get_response(request_topic)).lower()

    if 'weather' in response_topic:
        response_weather = await agent.get_response(message.text)
        await message.answer(response_weather)


@dp.message(F.content_type == 'audio')
async def audio_handler(message: types.Message):
    loop = asyncio.get_event_loop()
    audio = message.audio
    file_path = f'project/audio/{audio.file_id}.mp3'
    new_file = await bot.get_file(audio.file_id)
    file_url = f'https://api.telegram.org/file/bot{bot.token}/{new_file.file_path}'

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            if response.status == 200:
                async with aiofiles.open(file_path, 'wb') as file:
                    file_path = file.name
                    await file.write(await response.read())
                transcribe_text = await loop.run_in_executor(None, agent.get_transcribe, file_path)
                os.remove(file_path)
                await message.answer(transcribe_text)
            else:
                await message.answer('Error')
