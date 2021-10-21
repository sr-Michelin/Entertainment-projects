import random
import sqlite3
import telebot
from rezka_parser import sql
from telebot.types import Message, ReplyKeyboardMarkup

print("Bot RandomFilm is working...")

token = "#####################################"
bot = telebot.TeleBot(token)

genre_list = ['Драмы', 'Биографические', 'Приключения', 'Военные', 'Криминал', 'Боевики', 'Фантастика', 'Детективы',
              'Комедии', 'Триллеры', 'Мелодрамы', 'Фэнтези', 'Семейные', 'Вестерны', 'Исторические', 'Ужасы']


@bot.message_handler(commands=['start'])
def command_handler(message: Message):
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEDGXdhawtyhM_bHvBiqCkkefAiTiGDXwACzAADtIBKJP2ViLiQSME9IQQ")

    bot.send_message(message.chat.id, 'Привіт {0.first_name}) \nЯ <b>{1.first_name}</b> - '
                                      'бот, який допоможе Вам обрати фільм на вечір.'.
                     format(message.from_user, bot.get_me()), parse_mode='html')


@bot.message_handler(commands=['get_new'])
def command_handler(message: Message):
    bot.send_message(message.chat.id, f'Поповнення бази фільмів...')
    bot.send_message(message.chat.id, f'База поповнена: \n{sql(genre_="best", depth_=1)}')


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
            print('\nDatabase connected...')
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

                # c.execute('DELETE FROM best WHERE link = "{}"'.format(r_f[5]))
                # con.commit()

                # film_left = f'Залишилося фільмів жанру "{message.text}" - {len(film_list) - 1} шт'
                # bot.send_message(message.chat.id, film_left)
                # print(film_left)
                print(f'{message.from_user.id}, {message.from_user.username}, "{r_f[3]}", "{r_f[0]}"')

            else:
                bot.send_sticker(message.chat.id,
                                 "CAACAgIAAxkBAAEDGYRhawziXGhJxyhpEyjOy5-5_2O2sQACDgEAArSASiTg4WrIqh1AMCEE")
                bot.send_message(message.chat.id, f'Жанр "{message.text}" відсутній у базі...')

        except Exception as e:
            print(f'We have a problem: \n{e}')

        finally:
            con.close()
            print('Connection closed...')

    else:
        bot.send_sticker(message.chat.id,
                         "CAACAgIAAxkBAAEDGYRhawziXGhJxyhpEyjOy5-5_2O2sQACDgEAArSASiTg4WrIqh1AMCEE")
        bot.send_message(message.chat.id, f'"{message.text}" - невідома команда')
        print(f'{message.from_user.id}, {message.from_user.username}, "{message.text}"')


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
