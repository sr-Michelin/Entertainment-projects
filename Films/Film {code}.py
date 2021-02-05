import random
import webbrowser
import time

print('\nПрограма - "інтрига" для перегляду фільмів.')
try:
    fl1 = open('film_unwatched.txt', 'r')
    film = list(fl1)
    fl1.close()

    fr = random.randint(0, len(film) - 1)
    current_film = film[fr]

    print('\nЗараз глянемо {0}-й фільм: {1} '.format(fr + 1, current_film), end='')
    time.sleep(1)
    print('\bПуск!')
    time.sleep(1)
    webbrowser.open_new_tab(current_film)

    with open('film_unwatched.txt', 'r') as f:
        old_f = f.read()
    new_f = old_f.replace(current_film, '')
    with open('film_unwatched.txt', 'w') as f:
        f.write(new_f)
        f.close()

    print('Залишилося фільмів: %s шт.' % (len(film) - 1))

    film_w = open('film_watched.txt', 'a')
    film_w.write(current_film+'\n')
    film_w.close()

except ValueError:
    print('\nВітаю! Ви переглянули усі фільми.')
    time.sleep(1)
    webbrowser.open_new_tab('https://rezka.ag/')
    pass
input('\nДля закриття програми нажміть "Enter"')
