import sqlite3

from config import config_dict

conn = sqlite3.connect(config_dict["DATABASE"])
cursor = conn.cursor()
