from datetime import date, datetime
from dotenv import load_dotenv
import os
import requests
from database import db

load_dotenv()

people = db.extract_data() # getting people data from database

today = date.today().strftime("%d/%m/%Y").split("/")  # Getting actual year


def main():
    for person in people:  # for every person in the people list
        name = person[0]
        birthday = person[1].split("/")
        age = get_age(birthday[2], today[2])

        # calculating the days before the birthday
        remaining_days = datetime(
            year=int(today[2]), month=int(birthday[1]), day=int(birthday[0])
        ) - datetime(year=int(today[2]), month=int(today[1]), day=int(today[0]))
        if str(remaining_days)[0] == "-":
            remaining_days = datetime(
                year=int(today[2]) + 1, month=int(birthday[1]), day=int(birthday[0])
            ) - datetime(year=int(today[2]), month=int(today[1]), day=int(today[0]))
        remaining_days = remaining_days.days

        # scheduling reminders
        if remaining_days == 7:
            text = f"Il compleanno di {name} è tra {remaining_days} giorni, compirà {age} anni"
            send_reminder(text, person[2])
        elif remaining_days == 1:
            text = f"Il compleanno di {name} è domani!"
            send_reminder(text, person[2])
        elif remaining_days == 0:
            text = f"Il compleanno di {name} è oggi! Felici {age} anni!"
            send_reminder(text, person[2])


def get_age(birth_year, actual_year):  # calculating the age
    age = int(actual_year) - int(birth_year)
    return age


def send_reminder(text, chat_id):  # sending reminders to myself with a Telegram bot
    message = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={text}"
    return requests.get(message)


if __name__ == "__main__":
    main()
