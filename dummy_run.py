# import user_input
import user_database
# import python_wrapper
# import speech_errors
import numpy as np
import logging
from speech_errors import SpeechResult as enums
from speech_errors import SpeechProcessError, SpeechInvalidArgumentError
from time import time
# import android_actions as aa
import queue

table_names = []
android_input_data = []
business_input_data = []
supplies_input_data = []
data_tag = []

logging.basicConfig(level=logging.DEBUG)

android_actions = """ CREATE TABLE IF NOT EXISTS android_actions 
                                    (Size INT     NOT NULL,
                                    Length INT      NOT NULL,
                                    Occurrence  INT      NOT NULL,
                                    Name   TEXT    NOT NULL,
                                    Category            TEXT     NOT NULL);"""

android_words = """ CREATE TABLE IF NOT EXISTS android_words
                                    (Size INT     NOT NULL,
                                    Length INT      NOT NULL,
                                    Occurrence  INT      NOT NULL,
                                    Name   TEXT    NOT NULL,
                                    Category            TEXT     NOT NULL);"""

global_locations = """ CREATE TABLE IF NOT EXISTS global_locations
                                    (Size INT     NOT NULL,
                                    Length INT      NOT NULL,
                                    Occurrence  INT      NOT NULL,
                                    Name   TEXT    NOT NULL,
                                    Category            TEXT     NOT NULL);"""

adverb_table = """ CREATE TABLE IF NOT EXISTS adverb_table
                                    (Size INT     NOT NULL,
                                    Length INT      NOT NULL,
                                    Occurrence  INT      NOT NULL,
                                    Name   TEXT    NOT NULL,
                                    Category            TEXT     NOT NULL);"""

questions_tenses = """ CREATE TABLE IF NOT EXISTS questions_tenses
                                    (Size INT     NOT NULL,
                                    Length INT      NOT NULL,
                                    Occurrence  INT      NOT NULL,
                                    Name   TEXT    NOT NULL,
                                    Category            TEXT     NOT NULL);"""

businesses = """ CREATE TABLE IF NOT EXISTS businesses
                                    (Size INT     NOT NULL,
                                    Length INT      NOT NULL,
                                    Occurrence  INT      NOT NULL,
                                    Name   TEXT    NOT NULL,
                                    Category            TEXT     NOT NULL,
                                    Address        TEXT      NOT NULL,
                                    Updated_date         TEXT NOT NULL);"""

business_supplies = """ CREATE TABLE IF NOT EXISTS business_supplies
                                    (Size INT     NOT NULL,
                                    Length INT     NOT NULL,
                                    Occurrence  INT      NOT NULL,
                                    Name   TEXT    NOT NULL,
                                    Category            TEXT     NOT NULL,
                                    Brand         TEXT NOT NULL,
                                    Updated_date         TEXT NOT NULL);"""

business_actions = """ CREATE TABLE IF NOT EXISTS business_actions
                                    (Size INT     NOT NULL,
                                    Length INT      NOT NULL,
                                    Occurrence  INT      NOT NULL,
                                    Name   TEXT    NOT NULL,
                                    Category            TEXT     NOT NULL,
                                    Brand         TEXT NOT NULL,
                                    Updated_date         TEXT NOT NULL);"""

available_supplies = """ CREATE TABLE IF NOT EXISTS available_supplies
                                    (Size INT     NOT NULL,
                                    Length INT      NOT NULL,
                                    Occurrence  INT      NOT NULL,
                                    Name   TEXT    NOT NULL,
                                    Category            TEXT     NOT NULL,
                                    Brand         TEXT NOT NULL,
                                    Available_stores         TEXT NOT NULL,
                                    Updated_date         TEXT NOT NULL);"""

supply_add_ons = """ CREATE TABLE IF NOT EXISTS supply_add_ons
                                    (Size INT     NOT NULL,
                                    Length INT      NOT NULL,
                                    Occurrence  INT      NOT NULL,
                                    Name   TEXT    NOT NULL,
                                    Category            TEXT     NOT NULL,
                                    Brand         TEXT NOT NULL,
                                    Available_stores         TEXT NOT NULL,
                                    Updated_date         TEXT NOT NULL);"""

supply_descriptions = """ CREATE TABLE IF NOT EXISTS supply_descriptions
                                    (Size INT     NOT NULL,
                                    Length INT      NOT NULL,
                                    Occurrence  INT      NOT NULL,
                                    Name   TEXT    NOT NULL,
                                    Category            TEXT     NOT NULL,
                                    Brand         TEXT NOT NULL,
                                    Available_stores         TEXT NOT NULL,
                                    Updated_date         TEXT NOT NULL);"""


def read_input_db_file(db_file):
    try:
        with open(db_file, 'r') as file1:
            lines = file1.read().splitlines()
            words_lst = []
            global table_names, android_input_data, business_input_data, supplies_input_data, data_tag
            for line in lines:
                word_lst = line.split(",")
                # print(f"word_lst: {word_lst}")
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
                    # print(f"words_lst: {words_lst}")
                    android_input_data.append(words_lst)
                    # print(f"android_input_data: {android_input_data}")
                    words_lst = []
                    # print(f"android_input_data2: {android_input_data}")

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
                    # print(f"words_lst: {words_lst}")
                    business_input_data.append(words_lst)
                    # print(f"business_input_data: {business_input_data}")
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
                    # print(f"words_lst: {words_lst}")
                    supplies_input_data.append(words_lst)
                    # print(f"supplies_input_data: {supplies_input_data}")
                    words_lst = []
                else:
                    logging.error("Invalid tag or line in db file")

                word_lst.clear()
        logging.debug("Reading input db file success")
        return enums.SUCCESS.name
    except Exception as e:
        raise SpeechInvalidArgumentError(e)


def update_local_data_base(db_file):
    try:
        if read_input_db_file(db_file) == enums.FATAL_ERROR.name:
            return enums.FATAL_ERROR.name
        global table_names, android_input_data, business_input_data, supplies_input_data, data_tag
        res = enums.FAILURE.name
        a = 0
        b = 0
        s = 0
        for i, table in enumerate(table_names):
            # print(table)
            # print(type(table))
            # print(android_input_data[i])
            # print(type(android_input_data[i]))
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


def delete_local_db_data(table_name, data_):
    try:
        keys, index = convert_strings_to_num_array(data_)
        res = enums.FAILURE.name
        for i in range(0, len(keys)):
            # print(keys[i][0])
            res = g_db_obj.delete_db_data(table_name, keys[i][0], keys[i][2])
            if res != enums.SUCCESS.name:
                logging.error("Failed to delete data {0} from table {1}".format(keys[i][2], keys[i][0]))
        return res
    except Exception as e:
        raise SpeechProcessError(e)


def create_local_data_base(table_name):
    read_input_db_file("data.txt")
    try:
        res = enums.FAILURE.name
        for table in table_name:
            res = g_db_obj.create_table(eval(table))
            if res != enums.SUCCESS.name:
                logging.error("Failed to create table {}".format(table))
        return res
    except Exception as e:
        raise SpeechProcessError(e)


def show_data(table_name, data_):
    keys, index = convert_strings_to_num_array(data_)
    records = g_db_obj.fetch_db_data(table_name, keys[0][0])
    return records


query_type = ""
item_list = []
description = []
action_type = ""
location = "hillsboro"

words = []

g_db_obj = user_database.ProcessDataBaseRequests()

# r = read_input_db_file("data.txt")
# print(r)
connect = g_db_obj.create_connection()
# create_table = create_local_data_base(table_names)
# print(create_table)
# t = table_names[0]
# print(t)
# print(android_input_data)
# print(android_input_data[47])
# print(len(android_input_data))
# print(len(business_input_data))
# print(len(supplies_input_data))
# print(len(table_names))
# print(len(data_tag))

# for table in table_names:
# t = g_db_obj.create_table("android_actions")
# print(f"{t}")
#
# st = time()
# updatedata = update_local_data_base("data.txt")
# ft = time()
#
# print(updatedata)
# print(f"total time: {ft-st}")

# dele = delete_local_db_data("order")
# print(dele)
# print(table_names)

# delete = delete_local_db_data("supply_add_ons", "pizza")
# print(delete)
#
# fetch = g_db_obj.fetch_db_data("supply_add_ons", 558)
# print(f"fetch {fetch}")

# show = show_data("supply_add_ons", "turmeric")
# print(show)

q_t_ = queue.Queue(2)


def compare_input_string(string_input, compare_string):
    for i in range(len(string_input)):
        if string_input[i] != compare_string[i]:
            return False
    return True


def decode_user_input_for_android_actions(index, q_t):
    global words
    try:
        if index == 1 and get_android_actions(get_android_db_words("android_actions",
                                                                   index)):
            logging.debug("This is of intention to " + query_type + " android application")
            q_t.put(enums.SUCCESS.name)
        else:
            get_android_db_words("android_words", index)
            if not words:
                logging.error("No input user process")
                q_t.put(enums.INVALID_INPUT.name)
            else:
                word = words
                if check_android_command_status(index) == enums.INSUFFICIENT_INPUT.name:
                    if validate_android_action() is not None:
                        print("py wrapper not available")
                        # words = g_ui_obj.request_user_for_input(word)
                        # if words is None:
                        #     logging.error("Insufficient user input, could not process '{}'".format(word))
                        #     self.g_ui_obj.update_user_input_to_cloud(word)
                        #     q_t.put(enums.INVALID_INPUT.name)
                        # else:
                        #     if self.check_android_command_status(index) == enums.INSUFFICIENT_INPUT.name:
                        #         if self.validate_android_action() is not None:
                        #             q_t.put(enums.INVALID_INPUT.name)
                        #         else:
                        #             if self.validate_android_action() is not None:
                        #                 q_t.put(enums.INVALID_INPUT.name)
                        #             else:
                        #                 q_t.put(enums.SUCCESS.name)
                        #     else:
                        #         if self.validate_android_action() is not None:
                        #             q_t.put(enums.INVALID_INPUT.name)
                        #         else:
                        #             q_t.put(enums.SUCCESS.name)
                    else:
                        print(1)
                        q_t.put(enums.SUCCESS.name)
                else:
                    if validate_android_action() is not None:
                        q_t.put(enums.INVALID_INPUT.name)
                    else:
                        print(2)
                        q_t.put(enums.SUCCESS.name)
    except Exception as e:
        raise SpeechProcessError(e)


def get_android_actions(words_):
    try:
        if "order" == words_ or words_ is None:
            return None
        if words_ == data[0][2]:
            global query_type
            query_type = words_.decode('utf_8')
            return words_
        return None
    except Exception as e:
        raise SpeechProcessError(e)


def get_android_db_words(table, index):
    try:
        if index == 1:
            rows = g_db_obj.fetch_db_data(table, data[0][0])
            print(f"rows1: {rows}")
            if rows is not None:
                for r in rows:
                    if r[1] == data[0][1]:
                        if compare_input_string(r[3], data[0][2]):
                            print(f"get db word : {r[3]}")
                            words.append(r[3])
                            return r[3]
                return None
            else:
                logging.debug("This is of intention to " + query_type + " android application")
                print("and_db_word: none")
                return None
        for i in range(index):
            rows = g_db_obj.fetch_db_data(table, data[i][0])
            if rows is not None:
                for r in rows:
                    if r[1] == data[i][1]:
                        if compare_input_string(r[3], data[i][2]):
                            words.append(r[3])
        return None
    except Exception as e:
        raise SpeechProcessError(e)


def check_android_command_status(index):
    try:
        word_lst = words
        is_android_action = get_android_functions(word_lst)
        if is_android_action is not None:
            global query_type, action_type, location
            try:
                word_lst.remove(is_android_action)
            except(ValueError, Exception):
                is_android_action = is_android_action + "s"
                word_lst.remove(is_android_action)
            finally:
                pass
            if not word_lst and is_android_action != "weather":
                intention = "show"
                query_type = intention
                action_type = "android_action"
                item_list.append(is_android_action)
                logging.debug("This is an " + action_type + " of intention to " + query_type + " " + item_list[0].decode("utf_8"))
                return enums.SUCCESS.name
            else:
                intention = get_intention_type(word_lst, index)
                if intention is not None and intention == "order":
                    if is_android_action == "past" or is_android_action == "history":
                        query_type = "show"
                        action_type = "android_action"
                        item_list.append(intention + " " + "history")
                        logging.debug("This is an " + action_type + " of intention to " + query_type + " " +
                                      item_list[0].decode("utf_8"))
                        return enums.SUCCESS.name
                    else:
                        logging.warning("May be " + is_android_action + " is retailer action.")
                        return enums.INVALID_ANDROID_ACTION_TYPE.name
                elif is_android_action == "weather":
                    query_type = "show"
                    action_type = "android_action"
                    if get_location_for_weather_report(word_lst, index):
                        return enums.SERVICE_NOT_AVAILABLE.name
                    logging.debug("This is an " + action_type + " of intention to " + query_type + " " +
                                  item_list[0].decode("utf_8"))
                    return enums.SUCCESS.name
                elif intention is not None:
                    query_type = intention
                    action_type = "android_action"
                    item_list.append(is_android_action)
                    logging.debug("This is an " + action_type + " of intention to " + query_type + " " +
                                  item_list[0].decode("utf_8"))
                    return enums.SUCCESS.name
                else:
                    return enums.INVALID_ANDROID_ACTION_TYPE.name
        else:
            logging.info("This is not a android action")
            return enums.INVALID_ANDROID_ACTION_TYPE.name
    except Exception as e:
        raise SpeechProcessError(e)


def get_android_functions(words_):
    try:
        for word in data:
            if any(word[2] in s for s in words_):
                return word[2]
        return None
    except Exception as e:
        raise SpeechProcessError(e)


def get_intention_type(words_, index):
    try:
        get_android_db_words("Android_actions", index)
        action_list = words
        for word in action_list:
            if any(word in s for s in words_):
                return word
        return None
    except Exception as e:
        raise SpeechProcessError(e)


def get_location_for_weather_report(words_, index):
    try:
        global location
        current_location = location
        get_android_db_words("Global_locations", index)
        location = words[0].decode("utf_8")
        if not words_:
            item_list.append(current_location + " " + "weather")
            return enums.SUCCESS.name
        elif current_location != location:
            item_list.append(location + " " + "weather")
            return enums.SUCCESS.name
        else:
            logging.error("The location you are interested is not under countries we provide our services")
            return enums.INVALID_LOCATION.name
    except Exception as e:
        raise SpeechProcessError(e)


def validate_android_action():
    try:
        word = []
        if not action_type:
            word.append("android_action")
        if not query_type:
            logging.error("Android query type is not available")
            word.append("query_type")
        if not item_list:
            logging.error("Android item list is not available")
            word.append("item_list")
        if not description and check_android_description_need():
            logging.error("Android description is not available")
            word.append("description")
        if not word:
            return None
        else:
            return word
    except Exception as e:
        raise SpeechProcessError(e)


def check_android_description_need():
    if "photos" in item_list or "music" in item_list or "videos" in item_list:
        return True
    elif query_type == "play":
        return True
    else:
        return False


def generate_android_action_request():
    lis = [{"query_type": query_type}, {"item_list": item_list},
           {"description": description}, {"action_type": action_type}]
    return lis


data, index_ = convert_strings_to_num_array("mango")

dd = decode_user_input_for_android_actions(index_, q_t_)
print(f"dd: {dd}")
print(q_t_.get())


# gaar = generate_android_action_request()
# print(gaar)

business_name = ""
add_ons = []


def get_retail_db_words(table, index):
    try:
        if index == 1:
            rows = g_db_obj.fetch_db_data(table, data[0][0])
            if rows is not None:
                for r in rows:
                    if r[1] == data[0][1]:
                        if compare_input_string(r[3], data[0][2]):
                            words.append(r[3])
                            return r[3]
                return None
            else:
                logging.debug("This is of intention to " + query_type + " android application")
                return None
        for i in range(index):
            rows = g_db_obj.fetch_db_data(table, data[i][0])
            if rows is not None:
                for r in rows:
                    if r[1] == data[i][1]:
                        if compare_input_string(r[3], data[i][2]):
                            words.append(r[3])
        return None
    except Exception as e:
        raise SpeechProcessError(e)


def validate_user_input(index):
    incomplete = is_input_incomplete(index)
    word = []
    if incomplete is not None:
        for item in incomplete:
            word.append(item)
        return word
    return None


def is_input_incomplete(index):
    global query_type, business_name, item_list, add_ons, description
    result = []
    if query_type is None:
        result.append("query_type")
    if business_name is None:
        result.append("business_name")
    if not item_list:
        result.append("item_list")
    if item_list and not add_ons:
        if check_add_ons_need(index):
            result.append("add_ons")
        if check_description_need(index):
            result.append("description")
    if not result:
        return result
    return None


def check_add_ons_need(index):
    try:
        addon_req = get_retail_db_words("Supply_Add_ons", index)
        if addon_req is not None:
            return addon_req
        return None
    except Exception as e:
        raise SpeechProcessError(e)


def check_description_need(index):
    try:
        desc_need = get_retail_db_words("Supply_Descriptions", index)
        if desc_need is not None:
            return desc_need
        return None
    except Exception as e:
        raise SpeechProcessError(e)


def decode_user_input_for_retail_actions(index, q_t):
    try:
        if index == 1 and get_retail_actions(get_retail_db_words("Business_actions", index)):
            logging.warning("This is of intention to " + query_type + " business action and incomplete")
            """ Request for user input"""
            words_ = validate_user_input(index)
            # if ret_get_more_input(words_) == enums.SUCCESS.name:
            #     if check_retail_command_status(index) == enums.SUCCESS.name:
            #         if validate_user_input(index) is not None:
            #             q_t.put(enums.SUCCESS.name)
            #         else:
            #             q_t.put(enums.FAILURE.name)
            #     else:
            #         q_t.put(enums.FAILURE.name)
            # else:
            #     q_t.put(enums.FAILURE.name)
        else:
            if check_retail_command_status(index) == enums.SUCCESS.name:
                words_ = validate_user_input(index)
                print(f"check retail command status: {words_}")
                # if ret_get_more_input(words) == enums.SUCCESS.name:
                #     if check_retail_command_status(index) == enums.SUCCESS.name:
                #         if validate_user_input(index) is not None:
                #             q_t.put(enums.SUCCESS.name)
                #         else:
                #             q_t.put(enums.FAILURE.name)
                #     else:
                #         q_t.put(enums.FAILURE.name)
                # else:
                #     q_t.put(enums.FAILURE.name)
    except Exception as e:
        raise SpeechProcessError(e)


def get_retail_actions(words_):
    try:
        if words_ == data[0][2]:
            global query_type
            query_type = words_.decode("utf_8")
            return words_
        return None
    except Exception as e:
        raise SpeechProcessError(e)


# def ret_get_more_input(incomplete):
#     try:
#         if g_ui_obj.request_user_for_input(incomplete) == enums.FAILURE.name:
#             logging.error("Insufficient input from user, could not process the request '{}'".format(incomplete))
#             g_ui_obj.update_user_input_to_cloud(incomplete)
#             return enums.FAILURE.name
#         return enums.SUCCESS.name
#     except Exception as e:
#         raise SpeechInvalidArgumentError(e)


def check_retail_command_status(index):
    try:
        global business_name
        global item_list
        business_name = get_business_name(index)
        if business_name is not None:
            words.clear()
            item_list = get_business_supplies_list(index)
            if item_list is not None:
                words.clear()
        else:
            item_list = get_business_supplies_list(index)
            if item_list is not None:
                words.clear()
        global query_type
        query_type = get_business_action(index)
        if query_type is not None:
            words.clear()
        global description
        description = check_description_need(index)
        if description is not None:
            words.clear()
        global add_ons
        add_ons = check_add_ons_need(index)
        if add_ons is not None:
            words.clear()
    except Exception as e:
        raise SpeechProcessError(e)


def get_business_name(index):
    try:
        get_retail_db_words("Businesses", index)
        if not words:
            logging.debug("No business in user request")
            return None
        else:
            if len(words) == 1:
                return words[0]
            else:
                logging.debug("Notify user and get confirmation")
    except Exception as e:
        raise SpeechProcessError(e)


def get_business_action(index):
    try:
        get_retail_db_words("Business_actions", index)
        if not words:
            logging.debug("No business in user request")
            return None
        else:
            return words[0]
    except Exception as e:
        raise SpeechProcessError(e)


def get_business_supplies_list(index):
    try:
        global business_name
        if business_name is not None:
            get_retail_db_words(business_name.decode("utf_8")+"_supplies", index)
        else:
            get_retail_db_words("Available_supplies", index)
        if not words:
            logging.debug("No business in user request")
            return None
        else:
            return words
    except Exception as e:
        raise SpeechProcessError(e)


rand = decode_user_input_for_retail_actions(index_, q_t_)
print(rand)
print(q_t_.get())
