#@test_7876_bot
#kkuznetsov

import paramiko
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import logging
import os, re
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv

logging.basicConfig(filename='logfile1.txt', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', encoding="utf-8")

SERVER = os.getenv('SERVER')

load_dotenv()
TOKEN = os.getenv('TOKEN')
LOGIN = os.getenv('LOGIN')
PASSWD = os.getenv('PASSWORD')
PORT = os.getenv('PORT')

LOGIN_PSQL = os.getenv('LOGIN_PSQL')
PASSWD_PSQL = os.getenv('PASSWORD_PSQL_DB')
PORT_DB = os.getenv('PORT_PSQL')
SERVER_PSQL = os.getenv('SERVER_PSQL')
DB_PSQL = os.getenv('PSQL_DATABASE')


numbers_g = []
emails_g = ()

def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!, доступные команды: /uptime /ss /ps /uname /release /get_services /get_apt_list /find_email_func /find_phonenumber \
                              /df /free /mpstat /w /last /critical /auth /verify_password /get_emails /get_phone_numbers /get_repl_logs')

def find_email(update: Update, context): #команда поиска электропочты
    update.message.reply_text('Введи текст, содержащий адреса электропочты в формате XXXX@YYYY.ZZZ')    
    return 'find_email_func'


def find_email_func(update:Update, context): #поиск адреса электронной почты

    global emails_g

    user_input = update.message.text


    pattern_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_s = re.compile(pattern_email)
    email_list = email_s.findall(user_input)
    
    emails_g = email_list
    # Поиск адреса электронной почты в строке

    emails = ''
    for i in range(len(email_list)):
        emails += f'{i+1}. {email_list[i]}\n'

    if len(email_list)>0:
        update.message.reply_text(emails) #отправляем ответ на запрос
        update.message.reply_text('для записи всего этого в БД набери yes')
        return 'get_emails_toDB_command'
    else:
        update.message.reply_text('ничего нет((((((((((((((')
    return ConversationHandler.END


def find_phonenumber_command(update: Update, context): #команда поиска электропочты
    update.message.reply_text('Введи текст, содержащий номера телефонов в формате: \
                              8XXXXXXXXXX, 8(XXX)XXXXXXX, 8 XXX XXX XX XX, 8 (XXX) XXX XX XX, 8-XXX-XXX-XX-XX. Также вместо 8 на первом месте может быть +7')
    
    return 'find_phonenumber'

#def get_y_toDB_command(update: Update, context):
#    update.message.reply_text('Введи подтверждение yes для записи в БД')
#    
#    return 'y_toDB'

def emails_toDB(update: Update, context):


    answer_bot = update.message.text
    if answer_bot == 'yes':
        update.message.reply_text('записываю........................')
        insert_emails_to_db()
        update.message.reply_text('записано')
    else:
        update.message.reply_text('Ничего не записываю')
    return ConversationHandler.END


def y_toDB(update: Update, context):


    answer_bot = update.message.text
    if answer_bot == 'yes':
        update.message.reply_text('записываю........................')
        insert_to_db()
        update.message.reply_text('записано')
    else:
        update.message.reply_text('Ничего не записываю')
    return ConversationHandler.END

def insert_to_db():

    global numbers_g

    try:
        connection = psycopg2.connect(user=LOGIN_PSQL,
                                      password=PASSWD_PSQL,
                                      host=SERVER_PSQL,
                                      port=PORT_DB, 
                                      database=DB_PSQL)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM  tel_numbers")
        row = cursor.fetchall()
        index_db = 1
        for rows in row:
            index_db+=1
    except (Exception, Error) as error:
        print("NOT OK 1 Ошибка при работе с PostgreSQL", error)

    for number_db in numbers_g:
        print(number_db)
        try:
            SQL = "INSERT INTO  tel_numbers (personID, tel_number) VALUES (%s, %s);"
            data_insert = (index_db, number_db)
            cursor.execute(SQL, data_insert)
            connection.commit()

        except (Exception, Error) as error:
            print("NOT OK 2 Ошибка при работе с PostgreSQL", error)
        index_db+=1

    if connection:
        cursor.close()
        connection.close()
        print('соединение закрыто')
    else:
        print('чето не так с соединением')
    return True


def insert_emails_to_db():

    global emails_g

    try:
        connection = psycopg2.connect(user=LOGIN_PSQL,
                                      password=PASSWD_PSQL,
                                      host=SERVER_PSQL,
                                      port=PORT_DB, 
                                      database=DB_PSQL)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM  emails")
        row = cursor.fetchall()
        index_db = 1
        for rows in row:
            index_db+=1
    except (Exception, Error) as error:
        print("NOT OK 1 Ошибка при работе с PostgreSQL", error)

    for email_db in emails_g:
        print(email_db)
        try:
            SQL = "INSERT INTO  emails (personID, email) VALUES (%s, %s);"
            data_insert = (index_db, email_db)
            cursor.execute(SQL, data_insert)
            connection.commit()

        except (Exception, Error) as error:
            print("NOT OK 2 Ошибка при работе с PostgreSQL", error)
        index_db+=1

    if connection:
        cursor.close()
        connection.close()
        print('соединение закрыто')
    else:
        print('чето не так с соединением')
    return True

def find_phonenumber(update:Update, context):

    global numbers_g

    user_input = update.message.text


    pattern_phonenumber = r'[8|\+7][\- ]?\(?\d{3}\)?[\- ]?\d{3}[\- ]?\d{2}[\- ]?\d{2}'

    phonenumber_s = re.compile(pattern_phonenumber)
    phonenumber_list = phonenumber_s.findall(user_input)
    
    # Поиск адреса электронной почты в строке
    numbers_g = phonenumber_list
    update.message.reply_text(numbers_g) #отправляем ответ на запрос
#    update.message.reply_text('эта глобальная')
    phonenumbers = ''
    for i in range(len(phonenumber_list)):
        phonenumbers += f'{i+1}. {phonenumber_list[i]}\n'
          

    if len(phonenumber_list)>0:
        update.message.reply_text(phonenumbers) #отправляем ответ на запрос
        update.message.reply_text('для записи в БД введи yes')
        return 'get_y_toDB_command'
    else:
        update.message.reply_text('ничего нет((((((((((((((')
    return ConversationHandler.END


#проверка пароля
def verify_password_command(update: Update, context): #команда поиска электропочты
    update.message.reply_text('Введи пароль для проверки его сложности')
    
    return 'verify_password'
    

def verify_password(update:Update, context):
    password = update.message.text

    probe = re.compile(r'^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()-_]).{8,}$').findall(password)
    logging.info(probe)

    if len(probe)>0:
        update.message.reply_text('OK')
    else:
        update.message.reply_text('NOT OK')
    return ConversationHandler.END


#список пакетов
def get_apt_list_command(update: Update, context): #команда поиска списка пакетов
    update.message.reply_text('Введи название пакета для его поиска или all для вывода всего списка')
    
    return 'get_apt_list'


def search_packet(name, pack_list):
    for pack in pack_list:
        if pack.startswith(name):return True
    return False

def get_apt_list(update:Update, context):
    packet = update.message.text

    if packet == 'all':
        update.message.reply_text(ssh_connection('dpkg -l|awk \'{print $2}\'|tail -n 200'))
    else:
        if packet in ssh_connection('dpkg -l|awk \'{print $2}\'|tail -n 200'):
            update.message.reply_text('YEP')
        else:
            update.message.reply_text('NOPE')

#        update.message.reply_text(search_packet(packet, ssh_connection('dpkg -l|awk \'{print $2}\'|tail -n 200')))
#        update.message.reply_text('Поиск завершен чето другое надо')

    return ConversationHandler.END


def ssh_connection(command):
    client = paramiko.SSHClient() #не передается?
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Подключение к удаленному серверу
    try:
        client.connect(hostname=SERVER, username=LOGIN, password=PASSWD, port=PORT)
    except paramiko.AuthenticationException:
        return "Ошибка аутентификации. Проверьте логин и пароль."
    except paramiko.SSHException as e:
        return f"Ошибка подключения к серверу: {str(e)}"
    
    stdin, stdout, stderr = client.exec_command(command) 
    data = stdout.read() + stderr.read() 
    client.close()

    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1] 
    return data
    

def ssh_free(update: Update, context):
    user = update.effective_user

    update.message.reply_text(f'{user.full_name}, устанавливаем соединение с сервером............')
    update.message.reply_text(ssh_connection('free -h'))

def ssh_release(update: Update, context):
    update.message.reply_text(ssh_connection('lsb_release -a'))


def uname(update: Update, context):
    update.message.reply_text(ssh_connection('uname -a'))


def ssh_df(update: Update, context):
    update.message.reply_text(ssh_connection('df -h'))


def ssh_mpstat(update: Update, context):
    update.message.reply_text(ssh_connection('mpstat -A'))


def w(update: Update, context):
    update.message.reply_text(ssh_connection('w'))


def ssh_auths(update: Update, context):
    update.message.reply_text(ssh_connection('last')) 


def ssh_critical(update: Update, context):
    update.message.reply_text(ssh_connection('journalctl -xe -q|tail -n 5')) 


def ssh_ps(update: Update, context):
    update.message.reply_text(ssh_connection('ps -aux')) 


def ssh_ss(update: Update, context):
    update.message.reply_text(ssh_connection('ss -l|awk \'{print $5}\'')) 


def ssh_services(update: Update, context):
    update.message.reply_text(ssh_connection('systemctl list-units --type=service|awk \'{print $1}\'')) 

##LOGIN_PSQL = os.getenv('LOGIN_PSQL')
#PASSWD_PSQL = os.getenv('PASSWORD_PSQL_DB')
#PORT_DB = os.getenv('PORT_PSQL')
#DB_PSQL = os.getenv('PSQL_DATABASE')


def uptime(update: Update, context):
    update.message.reply_text(ssh_connection('uptime'))


def select_from_db(table_db, update: Update, context): #одна функция на почту и номера
    try:
        connection = psycopg2.connect(user=LOGIN_PSQL,
                                      password=PASSWD_PSQL,
                                      host=SERVER_PSQL,
                                      port=PORT_DB, 
                                      database=DB_PSQL)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM " + table_db)
        row = cursor.fetchall()
        for rows in row:
            update.message.reply_text(rows)
        update.message.reply_text('OKI OKI считано без ошибок')
    except (Exception, Error) as error:
        update.message.reply_text("NOT OK Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            update.message.reply_text('соединение с PG db закрыто')
        else:
            update.message.reply_text('чето не так с соединением')
    

def get_emails(update: Update, context):
    select_from_db('emails', update, context)


def get_phone_numbers(update: Update, context):
    select_from_db('tel_numbers', update, context)


def get_repl_logs(update: Update, context):

#    client = paramiko.SSHClient()
#    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Подключение к удаленному серверу
#    try:
#        client.connect(hostname='127.0.0.1', username='user', password='debian', port='2222')
#    except paramiko.AuthenticationException:
#        return "Ошибка аутентификации. Проверьте логин и пароль."
#    except paramiko.SSHException as e:
#        return f"Ошибка подключения к серверу: {str(e)}"
    
#    stdin, stdout, stderr = client.exec_command('tac /var/log/postgresql/postgresql-15-main.log |grep replication|head -n 10')
#    data = str(stdout.read() + stderr.read())
#    client.close()
    log_string = os.popen('cat /var/log/postgresql/postgresql-16-main.log').read()
    update.message.reply_text('работаем')
    update.message.reply_text(log_string)




def main():

    logging.info(TOKEN)

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # обработчик диалога
    # обработчик диалога поиска электропочты и телефона
    convHandlerFindEmail = ConversationHandler(entry_points=[CommandHandler('find_email_func', find_email)], states={'find_email_func':[MessageHandler(Filters.text & ~Filters.command, find_email_func)], \
                                                                                                                    'get_emails_toDB_command':[MessageHandler(Filters.text & ~Filters.command, emails_toDB)] }, fallbacks=[])
    convHandlerFindPhonenumber = ConversationHandler(entry_points=[CommandHandler('find_phonenumber', find_phonenumber_command)], states={'find_phonenumber':[MessageHandler(Filters.text & ~Filters.command, find_phonenumber)], \
                                                                                                                                          'get_y_toDB_command':[MessageHandler(Filters.text & ~Filters.command, y_toDB)]}, fallbacks=[])
    convHandlerVerify = ConversationHandler(entry_points=[CommandHandler('verify_password', verify_password_command)], states={'verify_password':[MessageHandler(Filters.text & ~Filters.command, verify_password)]}, fallbacks=[])
    convHandlerAptList = ConversationHandler(entry_points=[CommandHandler('get_apt_list', get_apt_list_command)], states={'get_apt_list':[MessageHandler(Filters.text & ~Filters.command, get_apt_list)]}, fallbacks=[])
#    convHandler_y_toDB = ConversationHandler(entry_points=[CommandHandler('y_toDB', get_y_toDB_command)], states={'y_toDB':[MessageHandler(Filters.text & ~Filters.command, y_toDB)]}, fallbacks=[])
    
    # Регистрируем обработчики команд	
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("free", ssh_free))
    dispatcher.add_handler(CommandHandler("release", ssh_release))
    dispatcher.add_handler(CommandHandler("uptime", uptime))
    dispatcher.add_handler(CommandHandler("uname", uname))
    dispatcher.add_handler(CommandHandler("df", ssh_df))
    dispatcher.add_handler(CommandHandler("mpstat", ssh_mpstat))
    dispatcher.add_handler(CommandHandler("w", w))
    dispatcher.add_handler(CommandHandler("auths", ssh_auths))
    dispatcher.add_handler(CommandHandler("critical", ssh_critical))
    dispatcher.add_handler(CommandHandler("ps", ssh_ps))
    dispatcher.add_handler(CommandHandler("ss", ssh_ss))
    dispatcher.add_handler(CommandHandler("get_services", ssh_services))
    dispatcher.add_handler(CommandHandler("get_emails", get_emails))
    dispatcher.add_handler(CommandHandler("get_phone_numbers", get_phone_numbers))
    dispatcher.add_handler(CommandHandler("get_repl_logs", get_repl_logs))

    dispatcher.add_handler(convHandlerFindEmail)
    dispatcher.add_handler(convHandlerFindPhonenumber)
    dispatcher.add_handler(convHandlerVerify)
    dispatcher.add_handler(convHandlerAptList)
 #   dispatcher.add_handler(convHandler_y_toDB)


    #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, ech
	# Запускаем бота
    updater.start_polling()

	# Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':

    logging.info('начинаем главный цикл_________________________________________')

    main()
