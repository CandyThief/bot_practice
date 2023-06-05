import telebot
import schedule

TOKEN = '6202722710:AAECGuVC9HR7AEQsO_fW5uo0D9aThnIFYF8'  # Замените на ваш токен бота

bot = telebot.TeleBot(TOKEN)

# Словарь для хранения интервалов напоминаний каждого пользователя
users_intervals = {}

# Интервал напоминания по умолчанию (4 часа)
DEFAULT_INTERVAL = 4 * 60  # в минутах

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привет! Я телеграм-бот, который будет напоминать тебе пить воду.")
    bot.send_message(chat_id, "Используй команду /setinterval <часы/минуты> для установки интервала напоминаний (например, /setinterval 2h или /setinterval 30m)")
    bot.send_message(chat_id, "Используй команду /reset для сброса интервала напоминаний и вернуться к интервалу по умолчанию.")
    bot.send_message(chat_id, "Используй команду /commands для просмотра доступных команд.")
    schedule_water_reminder(chat_id)  # Запускаем функцию для периодического напоминания

# Команда /setinterval
@bot.message_handler(commands=['setinterval'])
def set_interval(message):
    chat_id = message.chat.id
    try:
        interval_str = message.text.split()[1]  # Получаем строку интервала из сообщения пользователя
        interval = parse_interval(interval_str)  # Преобразуем строку в интервал времени
        if interval:
            users_intervals[chat_id] = interval  # Сохраняем интервал в словаре пользователей
            bot.send_message(chat_id, f"Интервал напоминаний установлен на {interval_str}.")
            schedule_water_reminder(chat_id)  # Перезапускаем напоминания с новым интервалом
        else:
            bot.send_message(chat_id, "Неверный формат интервала. Используйте <число>h для часов или <число>m для минут.")
    except IndexError:
        bot.send_message(chat_id, "Неверный формат команды. Используйте /setinterval <часы/минуты>.")

# # Команда /reset
# @bot.message_handler(commands=['reset'])
# def reset_interval(message):
#     chat_id = message.chat.id
#     users_intervals[chat_id] = None  # Сбрасываем интервал пользователя
#     bot.send_message(chat_id, "Интервал напоминаний сброшен.")

# Команда /commands
@bot.message_handler(commands=['commands'])
def show_commands(message):
    chat_id = message.chat.id
    commands = [
        "/start - Начать работу с ботом",
        "/setinterval <часы/минуты> - Установить интервал напоминаний о питье воды",
#        "/reset - Сбросить интервал напоминаний",
        "/commands - Просмотреть доступные команды"
    ]
    bot.send_message(chat_id, "Доступные команды:")
    bot.send_message(chat_id, "\n".join(commands))

# Функция для отправки напоминания
def send_water_reminder(chat_id):
    bot.send_message(chat_id, "Пора пить воду! 🚰")

# Функция для парсинга интервала времени
def parse_interval(interval_str):
    try:
        if interval_str.endswith("h"):
            hours = int(interval_str[:-1])
            return hours * 60  # Возвращаем интервал в минутах
        elif interval_str.endswith("m"):
            minutes = int(interval_str[:-1])
            return minutes  # Возвращаем интервал в минутах
        else:
            return None
    except ValueError:
        return None

# Функция для периодического напоминания
def schedule_water_reminder(chat_id):
    interval = users_intervals.get(chat_id, DEFAULT_INTERVAL)  # Получаем интервал из словаря пользователей (по умолчанию или установленный пользователем)
    schedule.clear(tag=chat_id)  # Очищаем расписание напоминаний для данного пользователя
    schedule.every(interval).minutes.do(send_water_reminder, chat_id=chat_id)  # Запускаем функцию отправки напоминания через указанный интервал

# Запуск бота
bot.polling()
