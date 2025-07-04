import os

from aiogram import Bot
from aiogram.types import FSInputFile

async def send_file_to_group(bot: Bot, chat_id: int, file_path: str):
    try:
        document = FSInputFile(file_path)
        await bot.send_document(chat_id=chat_id, document=document)
        print(f"✅ Отправлено в {chat_id}")
    except Exception as e:
        print(f"❌ Ошибка в {chat_id}: {e}")

