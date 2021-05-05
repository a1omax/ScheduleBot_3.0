import telebot
import db
import utils
import consts

from cfg import config_dict


bot = telebot.TeleBot(config_dict["BOT_TOKEN"],
                      parse_mode="markdown", threaded=False, skip_pending=True)


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
        bot.send_message(msg.chat.id, utils.get_schedule(group))


@bot.message_handler(commands=["tomorrow"])
def send_schedule_by_tomorrow(msg):
    group = db.return_value_from_DB(
        table="users", field="user_group", pivot="tg_user_id", pivot_value=msg.chat.id)

    if not group:
        bot.send_message(msg.chat.id, "Для начала укажите группу",
                         reply_markup=utils.create_reply_keyboard_markup(db.get_all_groups()))
    else:
        bot.send_message(msg.chat.id, utils.get_schedule(group, next_day=True))


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


@ bot.message_handler(commands=["group"])
def change_group(msg):
    bot.send_message(msg.chat.id, "Выберите Вашу группу",
                     reply_markup=utils.create_reply_keyboard_markup(db.get_all_groups()))
    db.change_value_in_DB(table="users", field_to_update="page",
                          field_to_update_value="input_group", pivot="tg_user_id", pivot_value=msg.chat.id)


@bot.message_handler(content_types=["text"])
def all_text(msg):
    page = db.return_value_from_DB(
        table="users", field="page", pivot="tg_user_id", pivot_value=msg.chat.id)

    if page == "input_group":
        db.change_value_in_DB(table="users", field_to_update="user_group",
                              field_to_update_value=msg.text, pivot="tg_user_id", pivot_value=msg.chat.id)

        bot.send_message(msg.chat.id, "Группа успешно обновлена")

        bot.send_message(msg.chat.id,
                         consts.MAIN_MESSAGE,
                         reply_markup=utils.create_inline_keyboard_markup(
                             kb=consts.MAIN_KB, group=msg.text),
                         )
        db.change_value_in_DB(table="users", field_to_update="page",
                              field_to_update_value="main", pivot="tg_user_id", pivot_value=msg.chat.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("day"))
def get_schedule_by_day_from_inline_kb(call):
    weekday_number = int(call.data.split("_")[1])
    group = db.return_value_from_DB(
        table="users", field="user_group", pivot="tg_user_id", pivot_value=call.message.chat.id)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=utils.get_schedule(group, weekday_number=weekday_number),
        reply_markup=utils.create_inline_keyboard_markup(kb=consts.BACK_KB),
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("back"))
def back(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Выберите день:",
        reply_markup=utils.create_inline_keyboard_markup(kb=consts.DAYS_KB),
    )

    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("today"))
def send_schedule_by_today_from_inline_kb(call):
    group = call.data.split("_")[1]

    bot.send_message(call.message.chat.id, utils.get_schedule(group))

    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("tomorrow"))
def send_schedule_by_tomorrow_from_inline_kb(call):
    group = call.data.split("_")[1]

    bot.send_message(call.message.chat.id,
                     utils.get_schedule(group, next_day=True))

    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == "all_days")
def send_schedule_by_today_from_inline_kb(call):
    bot.send_message(call.message.chat.id, "Выберите день:", reply_markup=utils.create_inline_keyboard_markup(
        kb=consts.DAYS_KB),
    )

    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == "group")
def select_group_from_inline_kb(call):
    bot.send_message(call.message.chat.id, "Выберите Вашу группу",
                     reply_markup=utils.create_reply_keyboard_markup(db.get_all_groups()))

    db.change_value_in_DB(table="users", field_to_update="page",
                          field_to_update_value="input_group", pivot="tg_user_id", pivot_value=call.message.chat.id)

    bot.answer_callback_query(call.id)
