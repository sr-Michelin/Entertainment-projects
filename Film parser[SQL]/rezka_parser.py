import regex as re
import sqlite3
import requests
from bs4 import BeautifulSoup


def parse(page=1, depth=1, genre='best', filter_='?filter=popular'):
    # Проміжний результат (у майбутньому треба позбутися)
    result = []

    while True:

        # Ключове посилання
        url = f"https://rezka.ag/films/{genre}/page/{page}/{filter_}"

        # Клієнт
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.116 Safari/537.36 OPR/69.0.3686.95'}

        HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        request = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(request.text, "html.parser")

        # HTML - результати
        films = soup.find_all("div", class_="b-content__inline_item-link")
        marks = soup.find_all("div", class_="b-content__inline_item-cover")

        # Перевірка умов пробігу сайту
        if page <= depth:
            if len(films) > 0:
                for film, mark in zip(films, marks):
                    # Блок кінцевих даних
                    title = film.find('a').text.strip()
                    year = film.find('div').text.split(', ')[0]
                    country = film.find('div').text.split(', ')[1]
                    genre_ = film.find('div').text.split(', ')[2]
                    link = film.find('a').get('href')
                    rate = re.split('[^0-9,.]', mark.find('i').get_text(strip=1))[-2] if genre == 'best' else None

                    result.append([title, year, country, genre_, rate, link])

                page += 1
            else:
                print(films)
                print(f'\nПереглянуті усі фільми категорії https://rezka.ag/films/{genre}')

        else:
            print(f'Переглянуті вибрані фільми ({len(result)}) категорії https://rezka.ag/films/{genre}')
            break

    return result


def sql(genre_='best', depth_=1):
    """Запис у БД SQLite"""

    try:
        with sqlite3.connect('rezka.db') as con:
            print('\nDatabase connected...')
            cursor = con.cursor()

            # Створення БД
            cursor.execute("""CREATE TABLE IF NOT EXISTS best(
            title VARCHAR(50),
            year INT,
            country VARCHAR(50),
            genre VARCHAR(50),
            rate FLOAT,
            link VARCHAR(100),
            Unique(title));""")

            # Огляд наявних записів у БД
            cursor.execute("""SELECT * FROM best""")

            Q = cursor.fetchall()
            q = [Q[i][0] for i in range(len(Q))]

            # Перевірка присутності майбутніх записів у списку існюючих
            for item in parse(genre=genre_, depth=depth_):
                if not item[0] in q:
                    cursor.execute("""INSERT INTO best VALUES (?,?,?,?,?,?)""", item)
                    con.commit()

            cursor.execute("""SELECT * FROM best""")
            Q2 = cursor.fetchall()
            # print(f'Записано {len(Q2) - len(Q)} фільмів')
            # return f'Записано {len(Q2) - len(Q)} нових фільмів із {depth_} (-и) сторінок'
            return f'Записано {len(Q2) - len(Q)} нових фільмів'

    except Exception as ex:
        print(ex)

    finally:
        print('Connection closed...')
        con.close()


if __name__ == '__main__':
    print(sql())
else:
    print('Module rezka_parser.py is connected...')
