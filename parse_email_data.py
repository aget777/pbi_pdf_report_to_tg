#!/usr/bin/env python
# coding: utf-8

import imaplib
import email
from email.header import decode_header
import config
import os
import sys
from datetime import datetime

file_path = config.email_file_path
file_path_storage = config.email_file_path

def get_connection():
    imap_server = config.imap_server
    imap_port = config.imap_port
    mail_pass = config.mail_pass
    username = config.username

    imap = imaplib.IMAP4_SSL(imap_server, imap_port)
    imap.login(username, mail_pass)
    return imap



def get_file_from_email(keyword):

    imap = get_connection()
    imap.select("INBOX")

    result, data = imap.search(None, f'(HEADER Subject "{keyword}")')
    if not data[0]:
        return sys.exit('Exiting the program')
    target_mail_id = data[0].split()[-1] # если несколько писем, то забираем последнее

    # если нужного письма нет, то выходим из программы
    if not target_mail_id:
        return sys.exit('Exiting the program')

    result, data = imap.fetch(target_mail_id, '(RFC822)') # забираем содержимое письма
    raw_email = data[0][1] # содержимое в закодированном виде

    try:
      email_message = email.message_from_string(raw_email)	
    except TypeError:
        email_message = email.message_from_bytes(raw_email)

    print ("--- нашли письмо от: ",email.header.make_header(email.header.decode_header(email_message['From'])))
    for part in email_message.walk():
        # проходим по содержимому письма
        if "application" in part.get_content_type():	    
            filename = part.get_filename()
            # создаем заголовок
            # filename=str(email.header.make_header(email.header.decode_header(filename)))
            # на всякий случай, если заголовка нет, то присваимваем свой
            # if not(filename): 
            #     filename = "weborama_report_X5_Perekrestok_Geo.xlsx"
            curr_date = datetime.now().date().strftime('%Y_%m_%d')
            filename = keyword + '_' + str(curr_date) + '.pdf'
            print (f'---- нашли вложение {filename}')
            fp = open(os.path.join(file_path, filename), 'wb')
            fp.write(part.get_payload(decode=1))
            fp.close

            fp2 = open(os.path.join(file_path_storage, filename), 'wb')
            fp2.write(part.get_payload(decode=1))
            fp2.close

            print ("-- удаляем письмо");
            imap.store(target_mail_id, '+FLAGS', '(\Deleted)')  
            imap.expunge()

    imap.close()
    imap.logout()


# In[ ]:


def get_text_from_email(keyword):
    # создаем подключение к почтовому ящику
    imap = get_connection()
    imap.select("INBOX")
    # находим письмо, в заголовке которого есть нужное нам ключевое слово
    result, data = imap.search(None, f'(HEADER Subject "{keyword}")')
    if not data[0]:
        return sys.exit('Exiting the program')

    # проходимся по списку писем и забираем каждое по отдельности
    for num, target_mail_id in enumerate(data[0].split()):
        # target_mail_id = data[0].split()[-1] # если несколько писем, то забираем последнее

        # если нужного письма нет, то выходим из программы
        if not target_mail_id:
            return sys.exit('Exiting the program')

        result, data = imap.fetch(target_mail_id, '(RFC822)') # забираем содержимое письма
        raw_email = data[0][1] # содержимое в закодированном виде

        try:
          email_message = email.message_from_string(raw_email)	
        except TypeError:
            email_message = email.message_from_bytes(raw_email)

        print ("--- нашли письмо от: ",email.header.make_header(email.header.decode_header(email_message['From'])))

    # если тело письма состоит из несколькиз частей, то проходим по каждой части отдельно
        if email_message.is_multipart():
            # print('Multipart types:')
            # for part in email_message.walk():
            #     print(f'- {part.get_content_type()}')
                # формруем список из типов контента, который содержится в каждой из частей
            multipart_payload = email_message.get_payload()
            for sub_message in multipart_payload:
                # нас интересует текст письма, который находится в формате HTML
                if sub_message.get_content_type()=='text/html':
                   # забираем текст в Бинарном формате
                    text = sub_message.get_payload(decode=1)
                   # сохраняем этот текст в отдельный файл
                    curr_date = datetime.now().date().strftime('%Y_%m_%d')
                    filename = 'email_' + str(curr_date) + '_' + str(num) + '.txt'
                    with open(os.path.join(file_path, filename), 'wb') as file:
                        try:
                            file.write(text)
                            print(f'Файл {filename} успешно сохранен')
                        except:
                            print('Ошибка при сохранении файла')

        else:  
            print('Данных для парсинга нет')

    imap.close()
    imap.logout()
