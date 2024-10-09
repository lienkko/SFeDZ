import telebot;
from methods import *
bot = telebot.TeleBot('7779947781:AAEApkVRU8d5EAyFECJ5y01r_ZCN5hCukjA')
weekdays = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота']
add_ts_date_flag = False
add_ts_sub_flag = False
add_ts_mes_flag = False
del_ts_flag = False
task_date = ''
task_sub = ''


def err(ch_id):
    bot.send_message(ch_id, 'Что-то пошло не так. Попробуйте еще раз',reply_markup=telebot.types.ReplyKeyboardRemove())

@bot.message_handler(commands=['del_task'])
def delete_task(message):
    f = open('admins_id.txt')
    ids = list(map(lambda x: x.split(':')[1], f.readlines()))
    if str(message.from_user.id) in ids:
        global tasks
        tasks = get_tasks()
        markup = telebot.types.ReplyKeyboardMarkup()
        for i in range(len(tasks)):
            markup.add(telebot.types.KeyboardButton(i+1)) 
        bot.send_message(message.chat.id, 'Какое задание вы бы хотели удалить?', reply_markup=markup)
        for i in range(len(tasks)):
            bot.send_message(message.chat.id, f'{i+1}   {tasks[i][2]} {tasks[i][3]}: {tasks[i][4]}')
        global del_ts_flag 
        del_ts_flag = True
        
@bot.message_handler(func=lambda mes: del_ts_flag and mes.content_type == 'text')
def op_delete_task(message):
    mes = message.text
    global del_ts_flag
    try:
        mes = int(mes)
        res = del_task(tasks[mes-1][0])
        if res:
            bot.send_message(message.chat.id,'Задание успешно удалено!',reply_markup=telebot.types.ReplyKeyboardRemove())
        else:
            err(message.chat.id)
    except:
        err(message.chat.id)
    del_ts_flag = False
        
@bot.message_handler(commands=['add_task'])
def add_new_date_ts(message):
    global add_ts_date_flag
    add_ts_date_flag = True
    bot.send_message(message.chat.id,'Введите дату в формате [День].[Месяц]')

@bot.message_handler(func=lambda mes: add_ts_date_flag and mes.content_type == 'text')
def add_new_date_ts(message):
    try: #Проверка даты
        t = message.text
        dt = t.split('.') 
        dt.append(str(datetime.today().year))
        dt = list(map(int,dt))
        bool(datetime.strptime(f'{dt[0]}-{dt[1]}-{dt[2]}','%d-%m-%Y'))
        if datetime.weekday(datetime(dt[2],dt[1],dt[0])) != 6:
            global task_date
            task_date = dt
        else:
            bot.send_message(message.chat.id, 'Это воскресенье')
            return
    except ValueError:
        bot.send_message(message.chat.id, 'Неправильный формат даты')
        return
    global add_ts_sub_flag
    global add_ts_date_flag
    global subs
    add_ts_sub_flag = True
    add_ts_date_flag = False
    subjects = get_subs()
    subs = []
    markup = telebot.types.ReplyKeyboardMarkup()
    for i in subjects:
        subs.append(i[0])
        markup.add(telebot.types.KeyboardButton(i[0])) 
    bot.send_message(message.chat.id, 'Какой предмет?', reply_markup=markup)

@bot.message_handler(func=lambda mes: add_ts_sub_flag and mes.content_type == 'text')
def add_new_sub_mes_ts(message):
    s=message.text
    if s not in subs:
        bot.send_message(message.chat.id, 'Неправильно введён предмет')
        return
    global task_sub
    global add_ts_sub_flag
    global add_ts_mes_flag
    task_sub = s
    add_ts_sub_flag = False
    add_ts_mes_flag = True
    bot.send_message(message.chat.id, "Введите задание:", reply_markup=telebot.types.ReplyKeyboardRemove())
    
@bot.message_handler(func=lambda mes: add_ts_mes_flag and mes.content_type == 'text')
def add_new_sub_mes_ts(message):
    m=message.text
    if make_task(task_date,task_sub,m):
        bot.send_message(message.chat.id,'Задание успешно добавлено!')
    else:
        err(message.chat.id)
    global add_ts_mes_flag
    add_ts_mes_flag = False
        

@bot.message_handler(commands=['get_hw'])
def get_all_tasks(message):
    mes = ''
    for task in get_tasks():
        mes += f"{task[1]} {task[2]} {task[3]}: {task[4]}\n"
    if mes == '':
        bot.send_message(message.chat.id, 'Пока нет ДЗ ;)')
        return
    bot.send_message(message.chat.id, mes)
        
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет!')
    bot.send_message(message.chat.id, 'Здесь ты можешь получить домашнее задание ФИИТ 1.4, написав команду /get_hw')

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Ты можешь получить домашнее задание ФИИТ 1.4, написав команду /get_hw')

@bot.message_handler(commands=['check_admins_id'])
def check_admins_id(message):
    with open('admins_id.txt') as f:
        ids = f.readlines()
        ids = list(map(lambda x: x.split(':')[1], ids))
        bot.send_message(message.chat.id, message.from_user.id)
#        for i in ids:
#            bot.send_message(message.chat.id, i)
    
    


bot.infinity_polling()