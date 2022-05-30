from bot import bot
from bot import consts
from bot import utils
from db import db


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
