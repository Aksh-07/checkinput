from builtins import any as s_any
import logging
from speech_errors import SpeechResult as enums
from speech_errors import SpeechProcessError
import user_database
import user_input

query_type = ""
item_list = []
description = []
action_type = ""
location = "hillsboro"

g_db_obj = user_database.ProcessDataBaseRequests()

class AndroidActions:
    def __init__(self, text_input):
        self.data = text_input
        self.words = []
        self.g_ui_obj = self.user_input_data_obj()
        g_db_obj.create_connection()

    def __del__(self):
        pass

    @staticmethod
    def user_input_data_obj():
        return user_input.ProcessUserInput()

    @staticmethod
    def compare_input_string(string_input, compare_string):
        for i in range(len(string_input)):
            if string_input[i] != compare_string[i]:
                return False
        return True

    def get_android_db_words(self, table, index):
        try:
            if index == 1:
                rows = g_db_obj.fetch_db_data(table, self.data[0][0])
                if rows is not None:
                    for r in rows:
                        if r[1] == self.data[0][1]:
                            if self.compare_input_string(r[3], self.data[0][2]):
                                self.words.append(r[3])
                                return r[3]
                    return None
                else:
                    logging.debug("This is of intention to " + query_type + " android application")
                    return None
            for i in range(index):
                rows = g_db_obj.fetch_db_data(table, self.data[i][0])
                if rows is not None:
                    for r in rows:
                        if r[1] == self.data[i][1]:
                            if self.compare_input_string(r[3], self.data[i][2]):
                                self.words.append(r[3])
            return None
        except Exception as e:
            raise SpeechProcessError(e)

    def decode_user_input_for_android_actions(self, index, q_t):
        try:
            if index == 1 and self.get_android_actions(self.get_android_db_words("Android_actions",
                                                                                 index)):
                logging.debug("This is of intention to " + query_type + " android application")
                q_t.put(enums.SUCCESS.name)
            else:
                self.get_android_db_words("Android_words", index)
                if not self.words:
                    logging.error("No input user process")
                    q_t.put(enums.INVALID_INPUT.name)
                else:
                    word = self.words
                    if self.check_android_command_status(index) == enums.INSUFFICIENT_INPUT.name:
                        if self.validate_android_action() is not None:
                            words = self.g_ui_obj.request_user_for_input(word)
                            if words is None:
                                logging.error("Insufficient user input, could not process '{}'".format(word))
                                self.g_ui_obj.update_user_input_to_cloud(word)
                                q_t.put(enums.INVALID_INPUT.name)
                            else:
                                if self.check_android_command_status(index) == enums.INSUFFICIENT_INPUT.name:
                                    if self.validate_android_action() is not None:
                                        q_t.put(enums.INVALID_INPUT.name)
                                    else:
                                        if self.validate_android_action() is not None:
                                            q_t.put(enums.INVALID_INPUT.name)
                                        else:
                                            q_t.put(enums.SUCCESS.name)
                                else:
                                    if self.validate_android_action() is not None:
                                        q_t.put(enums.INVALID_INPUT.name)
                                    else:
                                        q_t.put(enums.SUCCESS.name)
                        else:
                            q_t.put(enums.SUCCESS.name)
                    else:
                        if self.validate_android_action() is not None:
                            q_t.put(enums.INVALID_INPUT.name)
                        else:
                            q_t.put(enums.SUCCESS.name)
            
            # print(f"qzise in android action : {q_t.qsize()}")
        except Exception as e:
            raise SpeechProcessError(e)

    def check_android_command_status(self, index):
        try:
            word_lst = self.words
            is_android_action = self.get_android_functions(word_lst)
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
                    intention = self.get_intention_type(word_lst, index)
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
                        if self.get_location_for_weather_report(word_lst, index):
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

    def get_android_functions(self, words):
        try:
            for word in self.data:
                if s_any(word[2] in s for s in words):
                    return word[2]
            return None
        except Exception as e:
            raise SpeechProcessError(e)

    def get_android_actions(self, words):
        try:
            if "order" == words or words is None:
                return None
            if words == self.data[0][2]:
                global query_type
                query_type = words.decode('utf_8')
                return words
            return None
        except Exception as e:
            raise SpeechProcessError(e)

    def get_location_for_weather_report(self, words, index):
        try:
            global location
            current_location = location
            self.get_android_db_words("Global_locations", index)
            location = self.words[0].decode('utf_8')
            if not words:
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

    def get_intention_type(self, words, index):
        try:
            self.get_android_db_words("Android_actions", index)
            action_list = self.words
            for word in action_list:
                if s_any(word in s for s in words):
                    return word
            return None
        except Exception as e:
            raise SpeechProcessError(e)

    @staticmethod
    def generate_android_action_request():
        lis = [{"query_type": query_type}, {"item_list": item_list},
               {"description": description}, {"action_type": action_type}]
        return lis

    def validate_android_action(self):
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
            if not description and self.check_android_description_need():
                logging.error("Android description is not available")
                word.append("description")
            if not word:
                return None
            else:
                return word
        except Exception as e:
            raise SpeechProcessError(e)

    @staticmethod
    def check_android_description_need():
        if "photos" in item_list or "music" in item_list or "videos" in item_list:
            return True
        elif query_type == "play":
            return True
        else:
            return False
