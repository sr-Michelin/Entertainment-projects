# http://t.me/MS_film_bot

import datetime
import random
import sqlite3
import telebot
from rezka_parser import sql
from telebot.types import Message, ReplyKeyboardMarkup
import config

token = config.token
bot = telebot.TeleBot(token)
genre_list = config.genre_list


def _print(message, file="logs/logs.txt"):
    print(f'{message}')
    with open(file, "a+") as f:
        f.write(f"{message}\n")


_print("Bot MS_film is working...\n")


@bot.message_handler(commands=['start'])
def command_handler(message: Message):
    _print(
        f'{datetime.datetime.now()}: {message.from_user.id}, {message.from_user.first_name}, '
        f'{message.from_user.username}, "start"')
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEDGXdhawtyhM_bHvBiqCkkefAiTiGDXwACzAADtIBKJP2ViLiQSME9IQQ")
    bot.send_message(message.chat.id, 'Привіт {0.first_name}) \nЯ <b>{1.first_name}</b> - '
                                      'бот, який допоможе Вам обрати фільм на вечір.'.format(message.from_user,
                                                                                             bot.get_me()) +
                     f'{config.commands}',
                     parse_mode='html')


@bot.message_handler(commands=['get_count'])
def command_handler(message: Message):
    _print(
        f'{datetime.datetime.now()}: {message.from_user.id}, {message.from_user.first_name}, '
        f'{message.from_user.username}, "get_count"')
    bot.send_message(message.chat.id, f'Переглядаю кількість фільмів за жанрами...')
    with sqlite3.connect('rezka.db') as con:
        c, c_ = con.cursor(), con.cursor()
        c.execute('SELECT genre, count(*) FROM best group by genre order by count(*) DESC')
        c_.execute('SELECT count(*) FROM best')
    inf_c = str([{c[0]: c[1]} for c in c.fetchall()])[1:-1].replace("{", "").replace("}", "").replace("'", "").replace(
        ", ", ",\n")
    bot.send_message(message.chat.id, f'Знайшов: \n{inf_c}. \n\nВсього фільмів - {c_.fetchall()[0][0]}.')


@bot.message_handler(commands=['get_logs'])
def command_handler(message: Message):
    _print(
        f'{datetime.datetime.now()}: {message.from_user.id}, {message.from_user.first_name}, '
        f'{message.from_user.username}, "get_logs"')

    file = open("logs/logs.txt", 'rb')
    bot.send_message(message.chat.id, f'Надсилаю логи...')
    bot.send_document(message.chat.id, file)


@bot.message_handler(commands=['clear_logs'])
def command_handler(message: Message):
    with open("logs/logs.txt", "w") as f:
        f.write(
            f'{datetime.datetime.now()}: {message.from_user.id}, {message.from_user.first_name}, '
            f'{message.from_user.username}, "clear_logs"')
    file = open("logs/logs.txt", 'rb')
    bot.send_message(message.chat.id, f'Очищую логи...')
    bot.send_document(message.chat.id, file)


@bot.message_handler(commands=['get_new'])
def command_handler(message: Message):
    _print(
        f'{datetime.datetime.now()}: {message.from_user.id}, {message.from_user.first_name}, '
        f'{message.from_user.username}, "get_new"')
    bot.send_message(message.chat.id, f'Поповнення бази фільмів...')
    bot.send_message(message.chat.id, f'База поповнена: \n{sql(genre_="best", depth_=6)}')


@bot.message_handler(commands=['random'])
def command_handler(message: Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    for value in genre_list:
        markup.add(value)

    bot.send_message(message.chat.id, 'Виберіть жанр:', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def command_handler(message):
    if message.text in genre_list:
        bot.send_message(message.chat.id, f'Підбираю випадковий фільм жанру "{message.text}"...')

        try:
            _print('\nDatabase connected...')

            with sqlite3.connect('rezka.db') as con:
                c = con.cursor()
                c.execute(
                    'SELECT title,year,country,genre, rate, link FROM best WHERE genre = "{}"'.format(message.text))

            film_list = c.fetchall()

            if len(film_list) > 0:
                r_f = film_list[random.randint(0, len(film_list) - 1)]
                bot.send_sticker(message.chat.id,
                                 "CAACAgIAAxkBAAEDGX5hawu3CmVldfw58Ux_PAdw1_ceeQACyAADtIBKJN8urxC6_aPfIQQ")
                random_name = f'Зараз глянемо: \n{r_f[0]} ({r_f[1]}) \n{r_f[2]}, {r_f[3]}, {r_f[4]} \n\n{r_f[5]}'

                bot.send_message(message.chat.id, random_name)

                _print(
                    f'{datetime.datetime.now()}: {message.from_user.id}, {message.from_user.first_name}, '
                    f'{message.from_user.username}, "{r_f[3]}", "{r_f[0]}"')

            else:
                bot.send_sticker(message.chat.id,
                                 "CAACAgIAAxkBAAEDGYRhawziXGhJxyhpEyjOy5-5_2O2sQACDgEAArSASiTg4WrIqh1AMCEE")
                bot.send_message(message.chat.id, f'Жанр "{message.text}" відсутній у базі...')

        except Exception as e:
            _print(f'We have a problem: \n{e}')

        finally:
            con.close()
            _print('Connection closed...\n')

    else:
        bot.send_sticker(message.chat.id,
                         "CAACAgIAAxkBAAEDGYRhawziXGhJxyhpEyjOy5-5_2O2sQACDgEAArSASiTg4WrIqh1AMCEE")
        bot.send_message(message.chat.id, f'"{message.text}" - невідома команда')
        _print(
            f'{datetime.datetime.now()}: {message.from_user.id}, {message.from_user.first_name}, '
            f'{message.from_user.username}, "{message.text}" - невідома команда')


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
