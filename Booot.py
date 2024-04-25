import telebot
import random

bot = telebot.TeleBot('7118947135:AAEL-cPibN-tRFrSSFrif2cltypZrdHGm2k')

storage = dict()

def init_storage(user_id):
    storage[user_id] = dict( random_digit=None)

def set_data_storage(user_id, key, value):
    storage[user_id][key] = value

def get_data_storage(user_id):
    return storage[user_id]


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет)')
@bot.message_handler(commands=['play'])
def start_game(message):
    init_storage(message.chat.id)  ### Инициализирую хранилище

    attempt = 5
    set_data_storage(message.chat.id, "attempt", attempt)

    bot.send_message(message.chat.id, f'Игра "угадай число"!\nКоличество попыток: {attempt}')

    random_digit = random.randint(1, 10)
    print(random_digit)

    set_data_storage(message.chat.id, "random_digit", random_digit)
    print(get_data_storage(message.chat.id))

    bot.send_message(message.chat.id, 'Готово! Загадано число от 1 до 10!')
    bot.send_message(message.chat.id, 'Введите число')
    bot.register_next_step_handler(message, process_digit_step)

def process_digit_step(message):
    user_digit = message.text
    random_digit = get_data_storage(message.chat.id)["random_digit"]
    attempt = get_data_storage(message.chat.id)["attempt"]
    if not user_digit.isdigit():
        msg = bot.reply_to(message, 'Вы ввели не цифры, введите пожалуйста цифры')
        bot.register_next_step_handler(msg, process_digit_step)
        return
    if int(user_digit) == random_digit:
        bot.send_message(message.chat.id, f'Ура! Ты угадал число! Это была цифра: {random_digit}')
        init_storage(message.chat.id)  ### Очищает значения из хранилище
        return
    elif attempt > 1:
        if int(user_digit) < random_digit:
            bot.send_message(message.chat.id, 'Moе чиcло больше ')
        else:
            bot.send_message(message.chat.id, 'Мое число меньше')
        attempt -= 1
        set_data_storage(message.chat.id, "attempt", attempt)
        bot.send_message(message.chat.id, f'Неверно, осталось попыток: {attempt}')
        bot.register_next_step_handler(message, process_digit_step)
    else:
        bot.send_message(message.chat.id, 'Вы проиграли!')
        init_storage(message.chat.id)  ### Очищает значения из хранилище
        return


@bot.message_handler()
def gef_user_text(message):
    if message.text == "Как дела?":
        bot.send_message(message.chat.id, "Все отлично)))")
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю")



bot.polling(none_stop=True)