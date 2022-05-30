from bot import bot
from bot import consts
from bot import utils
from db import db


@bot.message_handler(commands=["start"])
def start(msg):
    db.set_start_page_or_ignore(msg.chat.id)

    group = db.return_value_from_DB(
        table="users", field="user_group", pivot="tg_user_id", pivot_value=msg.chat.id)

    if not group:
        bot.send_message(msg.chat.id, "Выберите Вашу группу",
                         reply_markup=utils.create_reply_keyboard_markup(db.get_all_groups()))
        db.change_value_in_DB(table="users", field_to_update="page",
                              field_to_update_value="input_group", pivot="tg_user_id", pivot_value=msg.chat.id)
    else:
        bot.send_message(msg.chat.id,
                         consts.MAIN_MESSAGE,
                         reply_markup=utils.create_inline_keyboard_markup(
                             kb=consts.MAIN_KB, group=group),
                         )
        db.change_value_in_DB(table="users", field_to_update="page",
                              field_to_update_value="main", pivot="tg_user_id", pivot_value=msg.chat.id)


@bot.message_handler(commands=["today"])
def send_schedule_by_today(msg):
    group = db.return_value_from_DB(
        table="users", field="user_group", pivot="tg_user_id", pivot_value=msg.chat.id)

    if not group:
        bot.send_message(msg.chat.id, "Для начала укажите группу",
                         reply_markup=utils.create_reply_keyboard_markup(db.get_all_groups()))
    else:
        bot.send_message(msg.chat.id, utils.get_schedule(
            group), reply_markup=utils.create_inline_keyboard_markup(kb=consts.MAIN_KB, group=group))


@bot.message_handler(commands=["tomorrow"])
def send_schedule_by_tomorrow(msg):
    group = db.return_value_from_DB(
        table="users", field="user_group", pivot="tg_user_id", pivot_value=msg.chat.id)

    if not group:
        bot.send_message(msg.chat.id, "Для начала укажите группу",
                         reply_markup=utils.create_reply_keyboard_markup(db.get_all_groups()))
    else:
        bot.send_message(msg.chat.id, utils.get_schedule(group, next_day=True),
                         reply_markup=utils.create_inline_keyboard_markup(kb=consts.MAIN_KB, group=group))


@bot.message_handler(commands=["day"])
def send_schedule_by_day(msg):
    group = db.return_value_from_DB(
        table="users", field="user_group", pivot="tg_user_id", pivot_value=msg.chat.id)

    if not group:
        bot.send_message(msg.chat.id, "Для начала укажите группу",
                         reply_markup=utils.create_reply_keyboard_markup(db.get_all_groups()))
    else:
        bot.send_message(msg.chat.id, "Выберите день:", reply_markup=utils.create_inline_keyboard_markup(
            kb=consts.DAYS_KB),
                         )


@bot.message_handler(commands=["group"])
def change_group(msg):
    bot.send_message(msg.chat.id, "Выберите Вашу группу",
                     reply_markup=utils.create_reply_keyboard_markup(db.get_all_groups()))
    db.change_value_in_DB(table="users", field_to_update="page",
                          field_to_update_value="input_group", pivot="tg_user_id", pivot_value=msg.chat.id)
