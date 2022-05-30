from bot import bot
from bot import consts
from bot import utils
from db import db


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
