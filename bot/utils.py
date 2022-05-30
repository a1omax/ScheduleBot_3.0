from datetime import datetime
from typing import List

from dateutil import tz
from dateutil.tz import tzoffset
from telebot import types

from db import db


def get_current_weekday_number() -> int:
    now = datetime.now()
    dt = datetime(month=now.month, year=now.year,
                  day=now.day, tzinfo=tz.gettz("Europe/Kiev"))

    return datetime.now(tzoffset(0, dt.utcoffset().seconds)).weekday()


def get_current_weekday_title_by_number(weekday_number: int) -> str:
    if weekday_number == 0:
        return "Понедельник"
    elif weekday_number == 1:
        return "Вторник"
    elif weekday_number == 2:
        return "Среда"
    elif weekday_number == 3:
        return "Четверг"
    elif weekday_number == 4:
        return "Пятница"
    elif weekday_number == 5:
        return "Суббота"
    elif weekday_number == 6:
        return "Воскресенье"


def get_current_week_type() -> str:
    return "odd" if datetime.now().isocalendar()[1] & 1 else "even"


def get_schedule(group: int, next_day: bool = False, weekday_number: int = -1) -> str:
    weekday_number = get_current_weekday_number() if weekday_number == - \
        1 else weekday_number
    weekday_number = (weekday_number + 1) % 7 if next_day else weekday_number

    subjects_info = db.return_all_subjects_info_by_group(
        group, weekday_number, get_current_week_type())

    if not subjects_info:
        return "Для указаной Вами группы нет расписания"
    else:
        msg_for_user = f"*{get_current_weekday_title_by_number(weekday_number)}*"

        for subject_info in subjects_info:
            title_and_cabinet_a = f"{subject_info[4]}\nКабинет: {subject_info[5]}" if subject_info[
                4] else "Нет пары"
            title_and_cabinet_b = f"{subject_info[6]}\nКабинет: {subject_info[7]}" if subject_info[
                6] else "Нет пары"
            msg_for_user += f"\n\n*{subject_info[3]} пара*\n*Подгруппа А:*\n{title_and_cabinet_a}\n*Подгруппа B:*\n{title_and_cabinet_b}"

        return msg_for_user


def create_inline_keyboard_markup(**kwargs: dict) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)

    inline_keyboard_buttons = [types.InlineKeyboardButton(
        text=text,
        callback_data=kwargs["kb"]["callbacks"][idx].format(**kwargs),
    ) for idx, text in enumerate(kwargs["kb"]["text"])]

    kb.add(*inline_keyboard_buttons)

    return kb


def create_reply_keyboard_markup(buttons: List[str]) -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)

    kb.add(*buttons)

    return kb
