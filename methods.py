import sqlite3
from datetime import datetime
 
def get_tasks(): #Функция для получения заданий
    connection = sqlite3.connect('DataBase/HomeWork.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Tasks')
    tasks = cursor.fetchall()
    connection.close()
    return tasks

def make_task(dt,sub,t): #Функция для записи заданий
    weekdays = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота']
    try:
        connection = sqlite3.connect('DataBase/HomeWork.db')
        cursor = connection.cursor()
        with connection:
            cursor.execute('INSERT INTO Tasks (wday, day, subject, task) VALUES (?, ?, ?, ?)', (f'{weekdays[datetime.weekday(datetime(dt[2],dt[1],dt[0]))]}', 
                                                                                                f'{dt[0]}-{dt[1]}',sub,t))
        connection.close()
    except Exception as e:
        print(e)
        return False
    return True

def del_task(id):
    try:
        connection = sqlite3.connect('DataBase/HomeWork.db')
        cursor = connection.cursor()
        with connection:
            cursor.execute(f'DELETE FROM Tasks WHERE id="{id}"')
        connection.close()
        return True
    except:
        return False
    
def get_subs():
    connection = sqlite3.connect('DataBase/HomeWork.db')
    cursor = connection.cursor()
    cursor.execute('SELECT subject FROM Subjects')
    subs = cursor.fetchall()
    connection.close()
    return subs