import time
import telebot
import bs4
from Task import Task
import parser_1
import markups as m
from aiogram import Bot, Dispatcher, executor, types

#main variables
TOKEN = "6282212419:AAFGxLS3vxlscXvh1CFNaYstR7ZmuzYiJP0"
bot = Bot(token=TOKEN)
task = Task()
dp = Dispatcher(bot=bot)

#handlers
@dp.message_handler(commands=['start', 'go'])
def start_handler(message):
    if not task.isRunning:
        chat_id = message.chat.id
        msg = dp.send_message(chat_id, 'Откуда парсить?', reply_markup=m.source_markup)
        dp.register_next_step_handler(msg, askSource)
        task.isRunning = True

def askSource(message):
    chat_id = message.chat.id
    text = message.text.lower()
    if text in task.names[0]:
        task.mySource = 'top'
        msg = dp.send_message(chat_id, 'За какой временной промежуток?', reply_markup=m.age_markup)
        dp.register_next_step_handler(msg, askAge)
    elif text in task.names[1]:
        task.mySource = 'all'
        msg = dp.send_message(chat_id, 'Какой минимальный порог рейтинга?', reply_markup=m.rating_markup)
        dp.register_next_step_handler(msg, askRating)
    else:
        msg = dp.send_message(chat_id, 'Такого раздела нет. Введите раздел корректно.')
        dp.register_next_step_handler(msg, askSource)
        return

def askAge(message):
    chat_id = message.chat.id
    text = message.text.lower()
    filters = task.filters[0]
    if text not in filters:
        msg = dp.send_message(chat_id, 'Такого временного промежутка нет. Введите порог корректно.')
        dp.register_next_step_handler(msg, askAge)
        return
    task.myFilter = task.filters_code_names[0][filters.index(text)]
    msg = dp.send_message(chat_id, 'Сколько страниц парсить?', reply_markup=m.amount_markup)
    dp.register_next_step_handler(msg, askAmount)

def askRating(message):
    chat_id = message.chat.id
    text = message.text.lower()
    filters = task.filters[1]
    if text not in filters:
        msg = dp.send_message(chat_id, 'Такого порога нет. Введите порог корректно.')
        dp.register_next_step_handler(msg, askRating)
        return
    task.myFilter = task.filters_code_names[1][filters.index(text)]
    msg = dp.send_message(chat_id, 'Сколько страниц парсить?', reply_markup=m.amount_markup)
    dp.register_next_step_handler(msg, askAmount)

def askAmount(message):
    chat_id = message.chat.id
    text = message.text.lower()
    if not text.isdigit():
        msg = dp.send_message(chat_id, 'Количество страниц должно быть числом. Введите корректно.')
        dp.register_next_step_handler(msg, askAmount)
        return
    if int(text) < 1 or int(text) > 5:
        msg = dp.send_message(chat_id, 'Количество страниц должно быть >0 и <6. Введите корректно.')
        dp.register_next_step_handler(msg, askAmount)
        return
    task.isRunning = False
    print(task.mySource + " | " + task.myFilter + ' | ' + text) #
    output = ''
    if task.mySource == 'top':
        output = parser_1.getTitlesFromTop(int(text), task.myFilter)
    else:
        output = parser_1.getTitlesFromAll(int(text), task.myFilter)
    msg = dp.send_message(chat_id, output, reply_markup=m.start_markup)


if __name__=='__name__' :
    executor.start_polling(dp)