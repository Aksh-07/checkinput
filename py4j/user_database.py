import logging
import sqlite3
from sqlite3 import Error
from speech_errors import SpeechResult as enums
from speech_errors import SpeechProcessError
import io
import numpy as np


def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_array(text_):
    out = io.BytesIO(text_)
    out.seek(0)
    return np.load(out, allow_pickle=True)


#  When inserting data, the array Convert to text Insert
sqlite3.register_adapter(np.ndarray, adapt_array)

#  When querying data, the text Convert to array
sqlite3.register_converter("array", convert_array)

database = r"user_tasks.db"


class ProcessDataBaseRequests:
    def __init__(self):
        self.conn = None

    def __del__(self):
        pass

    def create_connection(self):
        try:
            if self.conn is None:
                self.conn = sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
                logging.debug("connection created")
        except Error as e:
            raise SpeechProcessError(e)

    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            self.conn.commit()
            return enums.SUCCESS.name
        except Error as e:
            raise SpeechProcessError(e)

    def delete_table(self, table_name):
        try:
            c = self.conn.cursor()
            qstr = "DROP TABLE {0}".format(table_name)
            c.execute(qstr)
            self.conn.commit()
            return enums.SUCCESS.name
        except Error as e:
            raise SpeechProcessError(e)

    def insert_business_supplies_data(self, table_name, input_data):
        try:
            c = self.conn.cursor()
            qstr = "INSERT INTO {0} VALUES (?,?,?,?,?,?,?)".format(table_name)
            c.execute(qstr, input_data)
            self.conn.commit()
            return enums.SUCCESS.name
        except Error as e:
            raise SpeechProcessError(e)

    def insert_supplies_data(self, table_name, input_data):
        try:
            c = self.conn.cursor()
            qstr = "INSERT INTO {0} VALUES (?,?,?,?,?,?,?,?)".format(table_name)
            c.execute(qstr, input_data)
            self.conn.commit()
            return enums.SUCCESS.name
        except Error as e:
            raise SpeechProcessError(e)

    def insert_android_data(self, table_name, input_data):
        try:
            c = self.conn.cursor()
            qstr = "INSERT INTO {0} VALUES (?,?,?,?,?)".format(table_name)
            c.execute(qstr, input_data)
            self.conn.commit()
            return enums.SUCCESS.name
        except Error as e:
            raise SpeechProcessError(e)

    def fetch_db_data(self, table_name, input_key):
        try:
            c = self.conn.cursor()
            qstr = "SELECT * FROM {0} WHERE Size = ?".format(table_name)
            c.execute(qstr, (input_key,))
            records = c.fetchall()
            return records
        except Error as e:
            raise SpeechProcessError(e)

    def delete_db_data(self, table_name, input_key, input_data):
        try:
            records = self.fetch_db_data(table_name, input_key)
            print(f"delete {records}")
            key_value = None
            if records is not None:
                for row in records:
                    print(row)
                    if row[3] == input_data:
                        key_value = row[3]

                c = self.conn.cursor()
                qstr = "DELETE FROM {0} WHERE Name = ?".format(table_name)
                c.execute(qstr, (key_value,))
                self.conn.commit()
                return enums.SUCCESS.name
            else:
                return enums.DB_DELETE_ERROR.name

        except Error as e:
            raise SpeechProcessError(e)

