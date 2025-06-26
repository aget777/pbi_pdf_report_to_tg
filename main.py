import os
import pandas as pd
import asyncio
from time import sleep
from aiogram import Bot, Dispatcher
from aiogram.types import FSInputFile

import config
from tg_bot import send_file_to_group
from jup_main_email import get_powerbi_pdf_reports, clear_tmp_folder


BOT_TOKEN = config.bot_token

# Включаем отображение всех колонок
pd.set_option('display.max_columns', None)
# Задаем ширину столбцов по контенту
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

reports_link = config.reports_link
email_file_path = config.email_file_path


# забираем гугл csv с инфо об ИД групп и Токенов бота
df = pd.read_csv(reports_link)
df['pdf_report_name'] = df['pdf_report_name'].str.lower()

# Забираем PDF файлы с отчетами из почты
get_powerbi_pdf_reports()

async def main():
    bot = Bot(token=BOT_TOKEN)
    try:
        for i in os.listdir(email_file_path):
            report_name = i[:i.find('report') + 6].lower()

            # По названию отчета определяем ИД группы,в которую отправим отчет PDF
            group_id = int(list(df.query(f"pdf_report_name=='{report_name}'")['group_id'])[0])
            file_path = os.path.join(email_file_path, i)
            await send_file_to_group(bot, chat_id=group_id, file_path=file_path)
    finally:
        # ✅ Обязательно закрываем сессию!
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
    clear_tmp_folder()