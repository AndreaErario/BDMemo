from datetime import date, datetime
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

people = json.loads(os.environ["PEOPLE"]) # Format: [["name", "dd/mm/yyyy"], ["name", "dd/mm/yyyy"]]

today = date.today().strftime("%d/%m/%Y") # Getting actual year
today = today.split("/")

def main():
    for person in people: # for every person in the people list
        name = person[0]
        birthday = person[1]
        birthday = birthday.split("/")
        age = get_age(birthday[2], today[2])

        # calculating the days before the birthday
        remaining_days = datetime(year=int(today[2]),month=int(birthday[1]),day=int(birthday[0])) - datetime(year=int(today[2]), month=int(today[1]), day=int(today[0]))
        if str(remaining_days)[0] == "-":
            remaining_days = datetime(year=int(today[2])+1,month=int(birthday[1]),day=int(birthday[0])) - datetime(year=int(today[2]), month=int(today[1]), day=int(today[0]))
        remaining_days = remaining_days.days

        # scheduling reminders
        if remaining_days == 7:
            text = f"Il compleanno di {name} è tra {remaining_days} giorni, compirà {age} anni"
            send_reminder(text)
        if remaining_days == 1:
            text = f"Il compleanno di {name} è domani!"
            send_reminder(text)
        if remaining_days == 0:
            text = f"Il compleanno di {name} è oggi! Felici {age} anni!"
            send_reminder(text)     

def get_age(birth_year, actual_year): # calculating the age
    age = int(actual_year) - int(birth_year)
    return age

def send_reminder(text): # sending reminders to myself with a Telegram bot
    message = 'https://api.telegram.org/bot' + os.getenv("BOT_TOKEN") + '/sendMessage?chat_id=' + os.getenv("CHAT_ID") + '&parse_mode=Markdown&text=' + text
    send_message = requests.get(message)
    

if __name__ == "__main__":
    main()