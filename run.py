from bot import bot
from db import db

if __name__ == "__main__":
    db.create_users_table()

    bot.polling()
