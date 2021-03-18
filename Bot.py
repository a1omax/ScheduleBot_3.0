from cfg import *
from datetime import datetime
import telebot
from dateutil.tz import tzoffset
import sqlite3

bot = telebot.TeleBot(TOKEN)

# static vars time unused
para_start = [[7, 30], [9, 0], [10, 30], [12, 30], [14, 0], [15, 30], [16, 50], [18, 20]]
para_finish = [[8, 50], [10, 20], [11, 50], [13, 50], [15, 20], [16, 50], [18, 10], [19, 40]]

break_start = [[8, 50], [10, 20], [11, 50], [13, 50], [15, 20], [16, 50], [18, 10]]
break_finish = [[9, 0], [10, 30], [12, 30], [14, 0], [15, 30], [16, 50], [18, 20]]

dict_days = {
    0: ['monday', 'понедельник', 'пн', 'понеділок'],
    1: ['tuesday', 'вторник', 'вт', 'вівтор'],
    2: ['wednesday', 'среда', 'сред', 'ср', 'серед'],
    3: ['thursday', 'четверг', 'чт', 'четвер'],
    4: ['friday', 'пятница', 'пт', "п'ятниц", "пятниц"],
    5: ['saturday', 'суббота', 'сб ', 'субот', 'cуббот'],
    6: ['sunday', 'воскресенье', 'вс ', 'воскресенье', 'неділ']
}


def time_update():
    timezone = 2
    offset = tzoffset(None, timezone * 3600)  # offset in seconds
    global now, hour, minute, date
    now = datetime.now(offset)
    hour = int(now.strftime("%H"))
    minute = int(now.strftime("%M"))
    date = now.strftime("%m/%d/%Y, %H:%M:%S")


def the_day(value=0):
    return (now.weekday() + value) % 7


con = sqlite3.connect("schedule.db")
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
        tg_id TEXT,
        user_name TEXT,
        group_name TEXT, 
        register_date TEXT 
    )""")
con.commit()


def check_group(msg):
    con = sqlite3.connect("schedule.db")
    cur = con.cursor()

    tg_id = str(msg.from_user.id)
    gr_name = cur.execute("""SELECT group_name FROM users WHERE tg_id LIKE (?)""", (tg_id,)).fetchone()
    if gr_name:
        return gr_name[0]
    else:
        return 0


def set_group(msg):

    con = sqlite3.connect("schedule.db")
    cur = con.cursor()
    tg_id = str(msg.from_user.id)

    gr_name = cur.execute("""SELECT DISTINCT group_name FROM schedule""").fetchall()
    answer = (str(msg.text)).split(" ")
    for i in answer:
        for j in gr_name:
            if i == j[0]:

                if cur.execute("""SELECT group_name FROM users WHERE tg_id LIKE (?)""", (tg_id,)).fetchone():
                    cur.execute("""UPDATE users SET group_name = (?) WHERE tg_id LIKE (?)""", (i, tg_id))

                else:
                    cur.execute("""INSERT INTO users VALUES(?,?,?,?)""", (msg.from_user.id, msg.from_user.username,
                                                                          i, date))

                bot.reply_to(msg, "Группа успешно установлена на " + i, parse_mode="Markdown")
                con.commit()
                return 1

    else:
        suggests = ""
        for i in answer:
            i = "%" + i + "%"
            grp = cur.execute(
                """SELECT DISTINCT group_name FROM schedule WHERE group_name LIKE (?) ORDER BY group_name""",
                (i,)).fetchall()
            if grp:
                for g in grp:
                    suggests += "`" + g[0] + "`    "
        if suggests:
            bot.reply_to(msg, "Данной группы нет в базе. Может вы имели в виду: \n" \
                         + suggests + "\nПожалуйста, повторите попытку, нажав команду /group и укажите группу одну " \
                                      "из списка _(в точности как указано в списке)_", parse_mode="Markdown")
            return 2

        return 0


def week_now(change=0):
    week = (int(now.strftime("%V")) + ((int(now.strftime("%d")) + change) // 7)) % 2
    # Учебный год начинаться с четной недели (не совпадает)
    if week == 1:
        return "even"
    elif week == 0:
        return "odd"


def write_tg(first_gr, second_gr, day, message):
    to_write = "*" + dict_days[int(day)][1].capitalize() + "*"
    if first_gr:
        for i in range(len(first_gr)):
            if first_gr[i][1] is not None or second_gr[i][1] is not None:
                to_write += "\n\n*" + str(first_gr[i][0]) + " пара:*\n*Подгруппа А:* \n"
                if first_gr[i][1] is not None:
                    to_write += str(first_gr[i][1])
                    if first_gr[i][2] is not None:
                        to_write += "\nКабінет: " + str(first_gr[i][2])
                else:
                    to_write += "Нет пары"

                to_write += "\n*Подгруппа B:* \n"
                if second_gr[i][1] is not None:
                    to_write += str(second_gr[i][1])
                    if second_gr[i][2] is not None:
                        to_write += "\nКабінет: " + str(second_gr[i][2])
                else:
                    to_write += "Нет пары"
            else:
                to_write += "\n\n*" + str(first_gr[i][0]) + " пара:*\nНет пары"
        bot.reply_to(message, to_write, parse_mode='Markdown')
    else:
        bot.reply_to(message, "У вас нет пар")


def sched_named_day(message, day):
    grp = check_group(message)
    time_update()

    if grp:
        time_update()

        con = sqlite3.connect("schedule.db")
        cur = con.cursor()

        if day > the_day():
            week_type = week_now()
        else:
            week_type = week_now(7)

        day = str(day)

        first_gr = cur.execute(
            """SELECT number_para, name_para_first, cabinet_first FROM schedule WHERE group_name LIKE (?) AND week_day LIKE (?) and week_type LIKE (?) ORDER BY number_para""",
            (grp, day, week_type,)).fetchall()
        second_gr = cur.execute(
            """SELECT number_para, name_para_second, cabinet_second FROM schedule WHERE group_name LIKE (?) AND week_day LIKE (?) and week_type LIKE (?) ORDER BY number_para""",
            (grp, day, week_type,)).fetchall()

        write_tg(first_gr, second_gr, day, message)

    else:
        register_group(message)


def sched_by_day(message, day_change):
    grp = check_group(message)
    time_update()

    if grp:
        time_update()

        con = sqlite3.connect("schedule.db")
        cur = con.cursor()

        day = str(the_day(day_change))
        week_type = week_now(day_change)

        first_gr = cur.execute(
            """SELECT number_para, name_para_first, cabinet_first FROM schedule WHERE group_name LIKE (?) 
            AND week_day LIKE (?) and week_type LIKE (?) ORDER BY number_para""",
            (grp, day, week_type,)).fetchall()
        second_gr = cur.execute(
            """SELECT number_para, name_para_second, cabinet_second FROM schedule WHERE group_name LIKE (?) 
            AND week_day LIKE (?) and week_type LIKE (?) ORDER BY number_para""",
            (grp, day, week_type,)).fetchall()

        write_tg(first_gr, second_gr, day, message)

    else:
        register_group(message)


@bot.message_handler(commands=['today', 'сегодня'])
def para_today(message):
    sched_by_day(message, 0)


@bot.message_handler(commands=['tomorrow', 'завтра'])
def para_tomorrow(message):
    sched_by_day(message, 1)


def week_day(message):
    for word in message.text.lower().split(" "):
        for day in dict_days:
            for i in dict_days[day]:
                if word.find(i) != -1:
                    return day
    return -1


def check(message):
    day = week_day(message)

    if day != -1:
        sched_named_day(message, day)
    else:
        bot.reply_to(message, "Такого дня нет")


@bot.message_handler(commands=['day'])
def para_named_day(message):
    day = week_day(message)
    if day != -1:
        sched_named_day(message, day)

    else:
        msg = bot.reply_to(message, "Введите день недели: ")
        bot.register_next_step_handler(msg, check)


def check_grp(msg):

    reply = set_group(msg)
    if reply == 0:
        bot.reply_to(msg, "Неправильно указана группа или её нет в базе. Введите команду /group и укажите свою группу")


@bot.message_handler(commands=['group'])
def register_group(message):
    time_update()
    reply = set_group(message)
    if not reply:
        msg = bot.reply_to(message, "Введите номер вашей группы: ")
        bot.register_next_step_handler(msg, check_grp)


@bot.message_handler(commands=['start'])
def start_message(message):
    buttons = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=False, row_width=2)
    buttons.row('/today', '/tomorrow')
    buttons.row('/day', '/group')

    bot.send_message(message.from_user.id, "Бот расписания для ЧНУ\n\n*Команды:*\n"
                          "1. /today – выдает расисание на сегодня\n"
                          "2. /tomorrow – выдает расисание на сегодня\n"
                          "3. /day – выдает расисание на день недели\n"
                          "4. /group – записывает группу\n`Версия 3.1.2`\n`Создатель:` @A1omax", parse_mode='Markdown', reply_markup = buttons)


bot.polling(none_stop=True)
