import sqlite3

from cfg import config_dict
from typing import Union, List, Tuple


conn = sqlite3.connect(config_dict["DATABASE"])
cursor = conn.cursor()


def create_users_table() -> None:
    cursor.execute(
        """create table if not exists users(
            id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            tg_user_id integer UNIQUE,
            user_group text,
            page text NOT NULL,
            reg_date text
        )""",
    )

    conn.commit()


def set_start_page_or_ignore(tg_user_id: int) -> None:
    sql_stmt = "insert or ignore into users (reg_date, tg_user_id, page) values(datetime('now'), ?, ?)"

    cursor.execute(
        sql_stmt, (tg_user_id, "start"))

    conn.commit()


def change_value_in_DB(**kwargs: dict) -> None:
    sql_stmt = "update {table} set {field_to_update} = ? where {pivot}  = ?".format(
        **kwargs)

    cursor.execute(
        sql_stmt, (kwargs["field_to_update_value"], kwargs["pivot_value"]))

    conn.commit()


def return_value_from_DB(**kwargs: dict) -> Union[int, str, None]:
    sql_stmt = "select {field} from {table} where {pivot} = ?".format(
        **kwargs,
    )

    cursor.execute(sql_stmt, (kwargs["pivot_value"],))

    return cursor.fetchall()[0][0]


def return_all_subjects_info_by_group(group: str, weekday: int, week_type: str) -> List[Tuple[Union[str, int]]]:
    sql_stmt = "select * from schedule where group_name = ? and week_day = ? and week_type = ?"

    cursor.execute(sql_stmt, (group, str(weekday), week_type))

    return cursor.fetchall()


def get_all_groups() -> List[str]:
    sql_stmt = "select distinct group_name from schedule"

    cursor.execute(sql_stmt)

    return [row[0] for row in cursor.fetchall()]
