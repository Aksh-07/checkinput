from builtins import any as s_any
import logging
import queue
import string

from numpy import array
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
    def __init__(self, text_input: array):
        """stores parameter text_input into self.data, creates an empty list with name self.words,
        initiates self.user_input_data_obj() with variable name self.g_ui_obj, and creates an object of user_database.creates_connection()

        Args:
            text_input (array): array from function convert_strings_to_num_array(strings)
        """
        self.data = text_input
        self.words = []
        self.g_ui_obj = self.user_input_data_obj()
        g_db_obj.create_connection()

    def __del__(self):
        pass

    @staticmethod
    def user_input_data_obj():
        """creates an object of ProcessUserInput() class from user_input module

        Returns:
            object: object of user_input.ProcessUserInput() class
        """
        return user_input.ProcessUserInput()

    @staticmethod
    def compare_input_string(string_input: str, compare_string: str):
        """compare the user input string with the one fetched from databse

        Args:
            string_input (str): string fetched from database.
            compare_string (str): string entered by user.

        Returns:
            Boolean: TRUE - if string_input is same as compare_string
                     FALSE - if string_input is not same as compare_string
        """
        for i in range(len(string_input)):
            if string_input[i] != compare_string[i]:
                return False
        return True

    def get_android_db_words(self, table: str, index: int):
        """Fetch all the rows from given table with the given index then find the one that match the user input and stores 
        the string in self.words


        Args:
            table (str): table name to search and get data from.

            index (int): length of the array created by convert_strings_to_num_array(strings)

        Raises:
            SpeechProcessError: _description_

        Returns:
            bytes: r[3] if there is only one word in user input, 4th item of row is fetched from database which is a string converted into bytes.
            NONE: if there is no matching data found in database or there are more than one words in user input.
        """
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

    def decode_user_input_for_android_actions(self, index: int, q_t: queue):
        """Decode anp Process user input after getting an array and index from user_input.convert_strings_to_num_array(strings) and put results in queue q_t which can be either
        SUCCESS or INVALID_INPUT depending on conditions in the function.

        Args:
            index (int): length of the array created by convert_strings_to_num_array(strings)
            q_t (queue): object created from Queue.queue() class

        Raises:
            SpeechProcessError: _description_
        """
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
                            if words is enums.FAILURE.name:
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
        except Exception as e:
            raise SpeechProcessError(e)

    def check_android_command_status(self, index):
        """add items in intention, query_type, action_type and item list depending on diffrent conditions as mentioned in function if entered input is an android action.

        Args:
            index (int): length of the array created by convert_strings_to_num_array(strings)

        Raises:
            SpeechProcessError: _description_

        Returns:
            SUCCESS: If everything works fine
            INVALID_ANDROID_ACTION_TYPE: If entered user input is not an android action
            SERVICE_NOT_AVAILABLE: if user entered input is weather
        """
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
                if not word_lst and is_android_action != "weather".encode('utf_8'):
                    intention = "show"
                    query_type = intention
                    action_type = "android_action"
                    item_list.append(is_android_action.decode("utf_8"))
                    logging.debug("This is an " + action_type + " of intention to " + query_type + " " + item_list[0])
                    return enums.SUCCESS.name
                else:
                    intention = self.get_intention_type(word_lst, index)
                    if intention is not None and intention.decode('utf_8') == "order":
                        if is_android_action.decode('utf_8') == "past" or is_android_action.decode('utf_8') == "history":
                            query_type = "show"
                            action_type = "android_action"
                            item_list.append(intention.decode('utf_8') + " " + "history")
                            logging.debug("This is an " + action_type + " of intention to " + query_type + " " +
                                          item_list[0])
                            return enums.SUCCESS.name
                        else:
                            logging.warning("May be " + is_android_action.decode('utf_8') + " is retailer action.")
                            return enums.INVALID_ANDROID_ACTION_TYPE.name
                    elif is_android_action.decode('utf_8') == "weather":
                        query_type = "show"
                        action_type = "android_action"
                        if self.get_location_for_weather_report(word_lst, index):
                            logging.debug("This is an " + action_type + " of intention to " + query_type + " " +
                                      item_list[0])
                            return enums.SERVICE_NOT_AVAILABLE.name
                        return enums.SUCCESS.name
                    elif intention is not None:
                        query_type = intention.decode('utf_8')
                        action_type = "android_action"
                        item_list.append(is_android_action.decode("utf_8"))
                        logging.debug("This is an " + action_type + " of intention to " + query_type + " " +
                                      item_list[0])
                        return enums.SUCCESS.name
                    else:
                        return enums.INVALID_ANDROID_ACTION_TYPE.name
            else:
                logging.info("This is not a android action")
                return enums.INVALID_ANDROID_ACTION_TYPE.name
        except Exception as e:
            raise SpeechProcessError(e)

    def get_android_functions(self, words: list):
        """Match for any word in argument words present in self.data.

        Args:
            words (list): items in self.words after running get_android_db_words()

        Raises:
            SpeechProcessError: _description_

        Returns:
            bytes: string converted into bytes which is 3rd item in self.data
            NONE: if function condition does not work
        """
        try:
            for word in self.data:
                if s_any(word[2] in s for s in words):
                    return word[2]
            return None
        except Exception as e:
            raise SpeechProcessError(e)

    def get_android_actions(self, words: bytes):
        """enter item in query type if words match byte string in self.words and is not order or empty

        Args:
            words (bytes): returened value from get_android_db_words()

        Raises:
            SpeechProcessError: _description_

        Returns:
            NONE: if words == order or NONE
            words: if words == byte string stored in self.data
        """
        try:
            if "order".encode("utf_8") == words or words is None:
                return None
            if words == self.data[0][2]:
                global query_type
                query_type = words.decode('utf_8')
                return words
            return None
        except Exception as e:
            raise SpeechProcessError(e)

    def get_location_for_weather_report(self, words: bytes, index: int):
        """search global locations table for location name to get weather report

        Args:
            words (bytes): items in self.words after running get_android_db_words()
            index (int): length of the array created by convert_strings_to_num_array(strings)

        Raises:
            SpeechProcessError: _description_

        Returns:
            str: SUCCESS if current location is given or location is present in database
            str: INVALID_LOCATION if location is not present in database
        """
        try:
            global location
            current_location = location
            self.get_android_db_words("Global_locations", index)
            if not words:
                item_list.append(current_location + " " + "weather")
                return enums.SUCCESS.name
            elif words:
                location = words[0]
                if current_location != location:
                    item_list.append(location.decode('utf_8') + " " + "weather")
                    return enums.SUCCESS.name
                else:
                    item_list.append(current_location + " " + "weather")
                    return enums.SUCCESS.name
            else:
                logging.error("The location you are interested is not under countries we provide our services")
                return enums.INVALID_LOCATION.name
        except Exception as e:
            raise SpeechProcessError(e)


    def get_intention_type(self, words: bytes, index: int):
        """check for any matching word in argument words with words from table android actions

        Args:
            words (bytes): items in self.words after running get_android_db_words()
            index (int): length of the array created by convert_strings_to_num_array(strings)

        Raises:
            SpeechProcessError: _description_

        Returns:
            bytes: byte string word if any match
            NONE: if no match
        """
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
        """creates a list of dictionaries with keys `query_type`, `item_list`, `description`, `action_type` and its corresponding values 

        Returns:
            list: a list of dictionaries items with key value pairs
        """
        lis = [{"query_type": query_type}, {"item_list": item_list},
               {"description": description}, {"action_type": action_type}]
        return lis

    def validate_android_action(self):
        """put action_type, query_type, item_list, description values if not present

        Raises:
            SpeechProcessError: _description_

        Returns:
            NONE: if word list is NONE
            word: a list
        """
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
        """check for values in item_list and query_type

        Returns:
            boolean: True or FALSE depending on conditions
        """
        if "photos" in item_list or "music" in item_list or "videos" in item_list:
            return True
        elif query_type == "play":
            return True
        else:
            return False
