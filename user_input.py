"""import cv2
import numpy as np
from PIL import Image
import os, time
import logging
import json
from datetime import datetime
"""
import logging
import android_actions as aa
import retail_actions as ra
from speech_errors import SpeechResult as enums
from speech_errors import SpeechProcessError, SpeechInvalidArgumentError
from multiprocessing import Process, Lock, Value
import multiprocessing
from threading import Thread
import queue
import numpy as np
import user_database
import python_wrapper

"""sample = [[1, 3, "some", 5], [0, 2, 4, 6], [0, 59, "thing", 2], [9, 5, "yes", 2], [9, 8, "Ko", 6]]
for x in sample:
    print(x)
print("--------------------")
sample.append([19, 18, "NUM", 16])
for x in sample:
    print(x)"""

g_a_obj = None
g_r_obj = None

lock = Lock()
m_lock1 = Lock()
m_lock2 = Lock()
m_lock3 = Lock()

text_threads = Value('i', 0)
video_threads = Value('i', 0)
audio_threads = Value('i', 0)

table_names = []
android_input_data = []
business_input_data = []
supplies_input_data = []
data_tag = []

data_read = Value('i', 0)
files_accessed = Value('i', 0)

logging.basicConfig(level=logging.DEBUG)

g_db_obj = user_database.ProcessDataBaseRequests()


class BaseProcess(Process):
    def __init__(self, name=None, target=None, args=()):
        super().__init__()
        self.args = args
        self.target = target
        self.thread_name = name

    def __del__(self):
        pass


class AudioProcess(BaseProcess):
    count = 2


class VideoProcess(BaseProcess):
    count = 3


class TextProcess(BaseProcess):
    count = 1


class ProcessUserInput:
    def __init__(self):
        self.g_py_obj = self.py_wrapper_obj()

    def __del__(self):
        pass

    @staticmethod
    def py_wrapper_obj():
        return python_wrapper.PythonJavaBridge()

    def request_user_for_input(self, input_need):
        try:
            if self.g_py_obj.request_user_input_from_java(input_need):
                return enums.FAILURE.name
            return enums.SUCCESS.name
        except Exception as e:
            raise SpeechProcessError(e)

    def update_user_input_to_cloud(self, input_need):
        try:
            if self.g_py_obj.update_new_words_to_analysis(input_need):
                return enums.FAILURE.name
            return enums.SUCCESS.name
        except Exception as e:
            raise SpeechInvalidArgumentError(e)

    def start_audio_decode(self, data):
        pass

    def start_security_decode(self, data):
        pass

    @staticmethod
    def convert_strings_to_num_array(strings):
        try:
            strings = strings.lower()
            strings = strings.encode('utf_8')
            lst = strings.split()
            index = len(lst)
            words_lst = []
            for str1 in lst:
                arr = np.frombuffer(str1, dtype=np.uint8)
                data_arr = np.array(arr)
                word_lst = [np.sum(data_arr), data_arr.size, str1]
                words_lst.append(word_lst)
            return words_lst, index
        except Exception as e:
            raise SpeechProcessError(e)

    def decode_user_input(self, _string):
        try:
            if _string is None:
                return enums.INVALID_INPUT.name
            else:
                words, index = self.convert_strings_to_num_array(_string)
            global g_a_obj, g_r_obj
            q_t = queue.Queue(2)
            g_a_obj = aa.AndroidActions(words)
            g_r_obj = ra.RetailActions(words)
            and_t = Thread(target=g_a_obj.decode_user_input_for_android_actions, args=(index, q_t))
            ret_t = Thread(target=g_r_obj.decode_user_input_for_retail_actions, args=(index, q_t))
            and_t.start()
            ret_t.start()
            and_t.join()
            ret_t.join()
            ret_and = q_t.get()
            ret_ret = q_t.get()
            if ret_and != enums.SUCCESS.name:
                logging.debug("User intention is not a android action")
            elif ret_ret != enums.SUCCESS.name:
                logging.debug("User intention is not a retail action")
            elif ret_and == enums.SUCCESS.name:
                logging.debug("User intention is a android action")
                self.g_py_obj.process_user_intention_actions(g_a_obj.generate_android_action_request())
                return enums.SUCCESS.name
            elif ret_ret == enums.SUCCESS.name:
                logging.debug("User intention is a retail action")
                self.g_py_obj.process_user_intention_actions(g_r_obj.generate_retail_action_request())
                return enums.SUCCESS.name
            else:
                logging.debug("Unable to process user input")
                self.update_user_input_to_cloud(words)
            return enums.INVALID_INPUT.name
        except Exception as e:
            raise SpeechProcessError(e)

    def run(self, type_, _input):
        try:
            if type_ == "audio":
                at = Process(target=self.start_audio_decode, args=(_input,), name="Audio")
                at.start()
                m_lock1.acquire()
                at.join()
                m_lock1.release()
            elif type_ == "video":
                vt = Process(target=self.start_security_decode, args=(_input,), name="Video")
                vt.start()
                m_lock2.acquire()
                vt.join()
                m_lock2.release()
            elif type_ == "text":
                tt = Process(target=self.decode_user_input, args=(_input,), name="Text")
                tt.start()
                m_lock3.acquire()
                tt.join()
                m_lock3.release()
            else:
                for p in multiprocessing.active_children():
                    p.join()
            return 0
        except Exception as e:
            raise SpeechInvalidArgumentError(e)

    @staticmethod
    def read_input_db_file(db_file):
        try:
            with open(db_file, 'r') as file1:
                lines = file1.read().splitlines()
                words_lst = []
                global table_names, android_input_data, business_input_data, supplies_input_data, data_tag
                for line in lines:
                    word_lst = line.split(",")
                    if word_lst[0] == "android":

                        data_tag.append(word_lst[0])
                        table_names.append(word_lst[1])
                        strings = word_lst[3].encode('utf_8')
                        arr = np.frombuffer(strings, dtype=np.uint8)
                        data_arr = np.array(arr)
                        words_lst.append(np.sum(data_arr))
                        words_lst.append(data_arr.size)
                        occurrence = sum(x.count(np.sum(data_arr)) for x in android_input_data)
                        occurrence1 = sum(x.count(np.sum(data_arr)) for x in android_input_data)
                        if occurrence == occurrence1:
                            words_lst.append(occurrence)
                        else:
                            words_lst.append(1)
                        words_lst.append(strings)
                        words_lst.append(word_lst[4])
                        android_input_data.append(words_lst)
                        words_lst = []

                    elif word_lst[0] == "business":
                        data_tag.append(word_lst[0])
                        table_names.append(word_lst[1])
                        strings = word_lst[3].encode('utf_8')
                        arr = np.frombuffer(strings, dtype=np.uint8)
                        data_arr = np.array(arr)
                        words_lst.append(np.sum(data_arr))
                        words_lst.append(data_arr.size)
                        occurrence = sum(x.count(np.sum(data_arr)) for x in business_input_data)
                        occurrence1 = sum(x.count(np.sum(data_arr)) for x in business_input_data)
                        if occurrence == occurrence1:
                            words_lst.append(occurrence)
                        else:
                            words_lst.append(1)
                        words_lst.append(strings)
                        words_lst.append(word_lst[4])
                        words_lst.append(word_lst[5])
                        words_lst.append(word_lst[6])
                        business_input_data.append(words_lst)
                        words_lst = []

                    elif word_lst[0] == "supplies":
                        data_tag.append(word_lst[0])
                        table_names.append(word_lst[1])
                        strings = word_lst[3].encode('utf_8')
                        arr = np.frombuffer(strings, dtype=np.uint8)
                        data_arr = np.array(arr)
                        words_lst.append(np.sum(data_arr))
                        words_lst.append(data_arr.size)
                        occurrence = sum(x.count(np.sum(data_arr)) for x in supplies_input_data)
                        occurrence1 = sum(x.count(np.sum(data_arr)) for x in supplies_input_data)
                        if occurrence == occurrence1:
                            words_lst.append(occurrence)
                        else:
                            words_lst.append(1)
                        words_lst.append(strings)
                        words_lst.append(word_lst[4])
                        words_lst.append(word_lst[5])
                        words_lst.append(word_lst[6])
                        words_lst.append(word_lst[7])
                        supplies_input_data.append(words_lst)
                        words_lst = []
                    else:
                        logging.error("Invalid tag or line in db file")

                    word_lst.clear()
            logging.debug("Reading input db file success")
            return enums.SUCCESS.name
        except Exception as e:
            raise SpeechInvalidArgumentError(e)

    def update_local_data_base(self, db_file):
        try:
            if self.read_input_db_file(db_file) == enums.FATAL_ERROR.name:
                return enums.FATAL_ERROR.name
            global table_names, android_input_data, business_input_data, supplies_input_data, data_tag
            res = enums.FAILURE.name
            a = 0
            b = 0
            s = 0
            for i, table in enumerate(table_names):
                if data_tag[i] == "android":
                    res = g_db_obj.insert_android_data(table, android_input_data[a])
                    if res != enums.SUCCESS.name:
                        logging.error("Failed to update android data at index {0} in table {1}".format(a, table))
                    a += 1
                elif data_tag[i] == "business":
                    res = g_db_obj.insert_business_supplies_data(table, business_input_data[b])
                    if res != enums.SUCCESS.name:
                        logging.error("Failed to update business data at index {0} in table {1}".format(b, table))
                    b += 1
                elif data_tag[i] == "supplies":
                    res = g_db_obj.insert_supplies_data(table, supplies_input_data[s])
                    if res != enums.SUCCESS.name:
                        logging.error("Failed to update supplies data at index {0} in table {1}".format(s, table))
                    s += 1
                else:
                    logging.error("Invalid data at index in table {0}".format(table))
            return res
        except Exception as e:
            raise SpeechProcessError(e)

    def delete_local_db_data(self, table_name, data_):
        try:
            keys, index = self.convert_strings_to_num_array(data_)
            res = enums.FAILURE.name
            for i in range(0, len(keys)):
                res = g_db_obj.delete_db_data(table_name, keys[i][0], keys[i][2])
                if res != enums.SUCCESS.name:
                    logging.error("Failed to delete data {0} from table {1}".format(keys[i][2], keys[i][0]))
            return res
        except Exception as e:
            raise SpeechProcessError(e)

    @staticmethod
    def create_local_data_base(table_name):
        try:
            res = enums.FAILURE.name
            for table in table_name:
                res = g_db_obj.create_table(eval(table))
                if res != enums.SUCCESS.name:
                    logging.error("Failed to create table {}".format(table))
            return res
        except Exception as e:
            raise SpeechProcessError(e)


