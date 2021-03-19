import telebot
from telebot import types
import os
from dotenv import load_dotenv
from database import db
from datetime import datetime

load_dotenv()

bot = telebot.TeleBot(os.environ["BOT_TOKEN"])
start_time = datetime.utcnow()

person = []


@bot.message_handler(commands=["start"])  # on /start
def send_welcome(message):
    bot.reply_to(message, "Ciao! Grazie per avermi aggiunto, usa /help per iniziare")


@bot.message_handler(commands=["help"])  # on /help
def send_help(message):
    if datetime.utcfromtimestamp(message.date) < start_time:
        pass
    else:
        chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        add = types.InlineKeyboardButton("/add")
        remove = types.InlineKeyboardButton("/remove")
        list_command = types.InlineKeyboardButton("/list")
        markup.add(add, remove, list_command)
        bot.send_message(
            chat_id, "Ecco i comandi che puoi utilizzare:", reply_markup=markup
        )


@bot.message_handler(commands=["add"])  # on /add
def add_birthday(message):
    if datetime.utcfromtimestamp(message.date) < start_time:
        pass
    else:
        person.clear()
        chat_id = message.chat.id
        msg = bot.send_message(chat_id, "Chi sarà il festeggiato?")
        bot.register_next_step_handler(msg, set_name)


def set_name(message):
    if datetime.utcfromtimestamp(message.date) < start_time:
        pass
    else:
        chat_id = message.chat.id
        name = message.text
        person.append(name)
        msg = bot.send_message(chat_id, "Quando compie gli anni? Format: 00/00/0000")
        bot.register_next_step_handler(msg, set_date)


def set_date(message):
    if datetime.utcfromtimestamp(message.date) < start_time:
        pass
    else:
        chat_id = message.chat.id
        date = message.text
        try:
            datetime.strptime(date, "%d/%m/%Y")
            person.append(date)
            person.append(chat_id)
            msg = bot.send_message(chat_id, "Confermi? Si/No")
            bot.register_next_step_handler(msg, confirm)
        except:
            msg = bot.send_message(chat_id, "La data non è valida... Riprova")
            bot.register_next_step_handler(msg, set_date)


def confirm(message):
    if datetime.utcfromtimestamp(message.date) < start_time:
        pass
    else:
        chat_id = message.chat.id
        if message.text == "Si":
            try:
                db.insert_data(person[0], person[1], person[2])
                bot.send_message(
                    chat_id, "È ufficiale! ti ricorderò di questo compleanno"
                )
            except:
                bot.send_message(chat_id, "Mi dispiace, qualcosa è andato storto")
            person.clear()
        elif message.text == "No":
            person.clear()
            bot.send_message(chat_id, "Va bene, non ti notificherò")
        else:
            msg = bot.send_message(chat_id, "La risposta deve essere o Si o No")
            bot.register_next_step_handler(msg, confirm)


@bot.message_handler(commands=["remove"])  # on /remove
def remove_birthday(message):
    if datetime.utcfromtimestamp(message.date) < start_time:
        pass
    else:
        person.clear()
        msg = bot.send_message(message.chat.id, "Chi era il festeggiato?")
        bot.register_next_step_handler(msg, remove_name)


def remove_name(message):
    if datetime.utcfromtimestamp(message.date) < start_time:
        pass
    else:
        chat_id = message.chat.id
        name = message.text
        person.append(name)
        msg = bot.send_message(chat_id, "Quando compie gli anni? Format: 00/00/0000")
        bot.register_next_step_handler(msg, remove_date)


def remove_date(message):
    if datetime.utcfromtimestamp(message.date) < start_time:
        pass
    else:
        chat_id = message.chat.id
        date = message.text
        try:
            datetime.strptime(date, "%d/%m/%Y")
            person.append(date)
            person.append(chat_id)
            msg = bot.send_message(chat_id, "Confermi? Si/No")
            bot.register_next_step_handler(msg, remove_confirm)
        except:
            msg = bot.send_message(chat_id, "La data non è valida... Riprova")
            bot.register_next_step_handler(msg, remove_date)


def remove_confirm(message):
    if datetime.utcfromtimestamp(message.date) < start_time:
        pass
    else:
        chat_id = message.chat.id
        if message.text == "Si":
            try:
                if (person[0], person[1], str(person[2])) in db.extract_data():
                    db.delete_data(person[0], person[1], person[2])
                    bot.send_message(
                        chat_id, "Va bene, non notificherò più questo compleanno"
                    )
                else:
                    bot.send_message(
                        chat_id, "Il compleanno che vuoi eliminare non esiste"
                    )
            except:
                bot.send_message(chat_id, "Mi dispiace, qualcosa è andato storto")
            person.clear()
        elif message.text == "No":
            person.clear()
            bot.send_message(chat_id, "Va bene, non lo annullerò")
        else:
            msg = bot.send_message(chat_id, "La risposta deve essere o Si o No")
            bot.register_next_step_handler(msg, confirm)


@bot.message_handler(commands=["list"])  # on /list
def list_birthdays(message):
    if datetime.utcfromtimestamp(message.date) < start_time:
        pass
    else:
        data = db.extract_data()
        for x in data:
            if x[2] == str(message.chat.id):
                bot.send_message(message.chat.id, f"{x[0]}, {x[1]}")


bot.enable_save_next_step_handlers(delay=1)
bot.load_next_step_handlers()
bot.polling()
