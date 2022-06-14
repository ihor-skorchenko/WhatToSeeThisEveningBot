import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import random

bot = telebot.TeleBot('5503907616:AAG2KcYWdgvUcDo9pSUMSPln2y0jS0XwbW0')

url = 'https://www.kinonews.ru/top100/'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
req = requests.get(url, headers)

# with open('index.html', 'w') as file:
#     file.write(req.text)

with open('index.html') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

# find all film's titles
titles_list = []
titles = soup.find_all('a', class_='titlefilm')
for i in titles:
    titles_list.append(i.text)

# find all film's genres
genres_list = []
all_info = soup.find_all('div', class_='textgray')
for j in all_info:
    the_genre = j.find('span').text
    if the_genre == 'Жанр:':
        genres_list.append(j.find("a").text)

# find all film's posters
images_list = []
images = soup.find_all('div', class_='rating_leftposter')
for k in images:
    imgs = k.find('img').get('src')
    images_list.append('kinonews.ru' + imgs)

# necessary dictionaries
movies_and_genres_dict = dict(zip(titles_list, genres_list))
movies_and_posters_dict = dict(zip(titles_list, images_list))
movies_genres_posters_dict = dict(zip(titles_list, zip(genres_list, images_list)))

# to find all genres in set
types_genres = set()
for i in movies_and_genres_dict:
    types_genres.add(movies_and_genres_dict[i])


# function for random on the specified genre
def chosen_genre(one_of_genre):
    chosen_movie_list = []
    for movie, genre in movies_and_genres_dict.items():
        if genre == one_of_genre[:-2]:
            chosen_movie_list.append(movie)
    result = random.choice(chosen_movie_list)
    return result


# processing '/start' command
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton('БДЫЩ 🚀')
    markup.add(start_button)
    bot.send_message(message.chat.id,
                     'Привет, киноман! Я - генератор киношек на вечер. Если ты не можешь выбрать фильм, тогда скорее нажимай на кнопку.',
                     reply_markup=markup)


# processing all incoming messages
@bot.message_handler(content_types=['text'])
def choice_buttons(message):
    if message.chat.type == 'private':
        if message.text == 'БДЫЩ 🚀':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            choose_genre = types.KeyboardButton('Да, хочу выбрать жанр')
            just_random = types.KeyboardButton('Любой жанр')
            markup.add(choose_genre, just_random)
            bot.send_message(message.chat.id, 'Ты хочешь выбрать жанр?', reply_markup=markup)

        elif message.text == 'Любой жанр':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            watched_button = types.KeyboardButton('Уже смотрел, хочу выбрать другой фильм')
            well_done_button = types.KeyboardButton('Спасибо! Ушёл за попкорном :)')
            changed_genre = types.KeyboardButton('Хочу вернуться назад и выбрать жанр')
            markup.add(watched_button, well_done_button, changed_genre)
            bot.send_message(message.chat.id,
                             f'Сегодня ты будешь смотреть фильм в жанре {random.choice(list(types_genres))}',
                             reply_markup=markup)
            random_movie = random.choice(list(movies_genres_posters_dict))
            bot.send_message(message.chat.id, f'{random_movie}')
            bot.send_photo(message.chat.id, f'{movies_and_posters_dict[random_movie]}')

        elif message.text == 'Да, хочу выбрать жанр' or message.text == 'Хочу вернуться назад и выбрать жанр' or message.text == 'Хочу вернуться назад и выбрать другой жанр':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            drama = types.KeyboardButton('драма 🥀')
            for_children = types.KeyboardButton('детский 🧸')
            comedy = types.KeyboardButton('комедия 🎪')
            adventures = types.KeyboardButton('приключения 🏜')
            thriller = types.KeyboardButton('триллер 🎴')
            detective = types.KeyboardButton('детектив 🔍')
            military = types.KeyboardButton('военный 🪖')
            biography = types.KeyboardButton('биографический 👤')
            action = types.KeyboardButton('боевик 💣')
            back = types.KeyboardButton('Назад 🔙')
            markup.add(drama, for_children, comedy, adventures, thriller, detective, military, biography, action, back)
            bot.send_message(message.chat.id, 'Выбери жанр', reply_markup=markup)

        elif message.text == 'Уже смотрел, хочу выбрать другой фильм':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            watched_button = types.KeyboardButton('Уже смотрел, хочу выбрать другой фильм')
            changed_genre = types.KeyboardButton('Хочу вернуться назад и выбрать жанр')
            well_done_button = types.KeyboardButton('Спасибо! Ушёл за попкорном :)')
            markup.add(watched_button, well_done_button, changed_genre)
            bot.send_message(message.chat.id,
                             f'Сегодня ты будешь смотреть фильм в жанре {random.choice(list(types_genres))}',
                             reply_markup=markup)
            random_movie = random.choice(list(movies_genres_posters_dict))
            bot.send_message(message.chat.id, f'{random_movie}')
            bot.send_photo(message.chat.id, f'{movies_and_posters_dict[random_movie]}')

        elif message.text == 'Спасибо! Ушёл за попкорном :)':
            bot.send_message(message.chat.id, 'Приятного просмотра! 🍿')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            one_more_film = types.KeyboardButton('Выход в главное меню')
            markup.add(one_more_film)
            bot.send_message(message.chat.id, f'Хочешь выбрать еще один фильм и вернуться в главное меню?',
                             reply_markup=markup)

        elif message.text == 'Выход в главное меню' or message.text == 'Назад 🔙':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            choose_genre = types.KeyboardButton('Да, хочу выбрать жанр')
            just_random = types.KeyboardButton('Любой жанр')
            markup.add(choose_genre, just_random)
            bot.send_message(message.chat.id, 'Ты хочешь выбрать жанр?', reply_markup=markup)

        elif message.text == 'драма 🥀' or message.text == 'детский 🧸' or message.text == 'комедия 🎪' or message.text == 'приключения 🏜' or message.text == 'триллер 🎴' or message.text == 'детектив 🔍' or message.text == 'военный 🪖' or message.text == 'биографический 👤' or message.text == 'боевик 💣':
            markup = types.ReplyKeyboardMarkup(row_width=1)
            changed_genre = types.KeyboardButton('Хочу вернуться назад и выбрать другой жанр')
            well_done_button = types.KeyboardButton('Спасибо! Ушёл за попкорном :)')
            markup.add(well_done_button, changed_genre)
            this_genre = chosen_genre(message.text)
            bot.send_message(message.chat.id, f'Сегодня ты будешь смотреть фильм: {this_genre}', reply_markup=markup)
            bot.send_photo(message.chat.id, f'{movies_and_posters_dict[this_genre]}')

        else:
            bot.send_message(message.chat.id, f'Я тебя не понимаю 😢 Пожалуйста, выбери один из пунктов меню')


# function for infinite work of the bot
bot.polling(none_stop=True)
