import config
import telebot
import beautifulsoup

bot = telebot.TeleBot(config.token)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Да', 'Нет')


# При старте знакомство
@bot.message_handler(commands=['start'])
def start_message(message):
    s = 'CAACAgIAAxkBAAJYZV6n4sDP-9Ks-I3vMvX1Xd1EwCkvAAJfAgADOKAKRbnf8hWOy-kZBA'
    bot.send_sticker(message.chat.id, s)
    bot.send_message(
        message.chat.id,
        'Привет {}, добро пожаловать в бот HBootH, здесь я тебе помогу найти работу\n Напишите название работы'.format(
            message.from_user.first_name))


# Если ввести сообщение идет проверка на числа и ответ
@bot.message_handler(content_types=['text'])
def askAge(message):
    if message.text.lower() == 'нет':
        bot.send_message(message.chat.id, 'Жалко')
    elif message.text.lower() == 'да':
        bot.send_message(message.chat.id, 'Отлично')
    else:
        chat_id = message.chat.id
        text = message.text
        if text.isdigit():
            msg = bot.send_message(chat_id, 'Введите название а не число')
            bot.register_next_step_handler(msg, askAge)  # askSource
            return
        text = text_message(text)
        parcs = beautifulsoup.parse(f'https://hh.ru/search/vacancy?area=1&st=searchVacancy&text={text}')
        ssf = parcs
        for j in ssf:
            markup = telebot.types.InlineKeyboardMarkup()
            btn_my_site = telebot.types.InlineKeyboardButton(text='Перейти на сайт', url=j[1])
            markup.add(btn_my_site)
            bot.send_message(chat_id, j[0], reply_markup=markup)
        bot.send_message(chat_id, 'Нашли что-нибудь полезное?', reply_markup=keyboard1)


def text_message(message):
    text = message
    lst = text.split()
    text = ''

    for i in lst:
        g = f"{i}+"
        text += g
    return text

if __name__ == '__main__':
    bot.infinity_polling()
