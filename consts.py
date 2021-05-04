# Keyboards
MAIN_KB = {
    "text": ["Today", "Tomorrow", "Day", "Group"],
    "callbacks": ["today_{group}", "tomorrow_{group}", "all_days", "group"],
}
DAYS_KB = {
    "text": ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"],
    "callbacks": ["day_0", "day_1", "day_2", "day_3", "day_4", "day_5", "day_6"],
}
BACK_KB = {
    "text": ["◀️ Назад"],
    "callbacks": ["back"],
}

# Messages
MAIN_MESSAGE = """Бот расписания для ЧНУ
*Команды:*
1. /today – выдает расписание на сегодня
2. /tomorrow – выдает расписание на завтра
3. /day – выдает расписание на день недели
4. /group – выбор группы
`Версия 3.2`
`Создатель:` @A1omax
"""
