#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os

from time import sleep
import numpy as np
from datetime import date
from datetime import datetime


import config
from parse_email_data import get_file_from_email

# Включаем отображение всех колонок
pd.set_option('display.max_columns', None)
# Задаем ширину столбцов по контенту
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)


"""
Функция для удаления файлов из временных папок
"""
def clear_tmp_folder(files_folder=config.email_file_path):
    # здесь запускаем логику удаления CSV файлов
    if 'files' in files_folder:
        if os.listdir(files_folder):
            # достаем каждый отдельный файл
            for file_name in os.listdir(files_folder):
                os.remove(os.path.join(files_folder, file_name))


# In[11]:


def get_powerbi_pdf_reports():
    clear_tmp_folder()
    for bot, reports_list in config.tg_bot_reports_dict.items():
        for keyword in reports_list:
            try:
                get_file_from_email(keyword)
            except:
                print(f'Отчет не найден: {keyword}')

