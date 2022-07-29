from distutils.text_file import TextFile
from py4j.java_gateway import JavaGateway,GatewayParameters
import user_input as py_obj
from datetime import datetime
from speech_errors import SpeechResult as enums
from speech_errors import SpeechProcessError, SpeechInvalidArgumentError
import logging



questions = ["can", "should", "would", "what", "when", "where", "how", "who", "whose", "why", "which", "isn't", "don't",
             "aren't", "won't", "must"]
locations = ["united states of america", "usa", "uk", "united kingdom"]
tenses = ["is", "are", "will", "shall", "did", "have", "had", "has", "were"]
adverb = ["good", "open", "closed", "shutdown", "giving", "asking", "accepting", "delivering", "address"]
actions = ["show", "order", "get", "add", "cancel", "decline", "dismiss", "stop", "close", "play", "pause", "up",
           "down", "change", "save", "repeat", "shuffle", "seek", "enable", "open", "ask", "accept", "delivering",
           "back", "forward", "connect"]
android_word = ["photo", "video", "memories", "memory", "history", "past", "weather", "music", "setting", "calendar",
                 "weather", "volume", "display", "wallpaper", "screen", "saver", "profile", "picture", "notification",
                 "promotion", "date", "time", "year", "month", "temperature", "network", "wifi", "bluetooth",
                 "seconds", "minutes", "hours", "favorites", "album", "silent", "mode", "brightness", "preference",
                 "security", "camera", "cam", "camera1", "cam1", "camera2", "cam2", "camera3", "cam3", "camera4",
                 "cam4", "security", "card", "credit", "debit", "pin", "cvv", "address", "apartment", "home",
                 "emergency"]

retailers = ["costco", "kfc", "bjs", "target"]
ret_actions = ["order", "get", "add", "cancel", "stop", "take", "over"]
incomplete_actions = ["order", "get", "add", "cancel", "take", "over"]
restaurants = [""]
brands = ["nike"]
accessories = [""]
apparels = [""]
furniture = [""]
electronics = [""]
electrical = [""]
office_supplies = []
toys = []
school = []
college = []
pharma = []
cosmetics = []
snacks = []
fruits = []
diary = []
groceries = []
vegetables = []
automotive = []
women_clothing = []
men_clothing = []
optical_frames = []
sports = []


gateway = JavaGateway(gateway_parameters=GatewayParameters(auto_convert=True))
# speech_process = gateway.jvm.py4j.examples.AppClass()
speech_process = gateway.jvm.py4j.AppClass()


class PythonSpeechWrapper:
    def __init__(self):
        """creates an object of ProcessUserInput() class from user_input module
        """
        self.user_obj = py_obj.ProcessUserInput()

    def __del__(self):
        pass

    def get_user_input(self, data_type: str, input_data: str):
        """calls and compare the results from self.user_obj.run() with data_type and input_dta as argument

        Args:
            data_type (str): `audio`, `video` or `text`
            input_data (str): user input

        Raises:
            SpeechProcessError: _description_

        Returns:
            int: 1 if self.user_obj.run() fails
                 0 if self.user_obj.run() is success
        """
        try:
            start_time = datetime.now()
            if self.user_obj.run(data_type, input_data) == 0:
                logging.error("Failed to start speech process")
                return 1
            logging.debug("Total execution time : %s " % (datetime.now() - start_time))
            return 0
        except Exception as e:
            raise SpeechProcessError(e)

    def update_local_db(self, db_file: TextFile):
        """calls update_local_data_base() function from user_input module

        Args:
            db_file (TextFile): .txt file to read data from

        Raises:
            SpeechInvalidArgumentError: _description_

        Returns:
            str : result from update_local_data_base() function from user_input module
        """
        try:
            return self.user_obj.update_local_data_base(db_file)
        except Exception as e:
            raise SpeechInvalidArgumentError(e)

    def create_local_db_tables(self, table_names: list):
        """calls create_local_data_base() from user_input module to create local database with given table names

        Args:
            table_names (list): list of tables to be created in database

        Returns:
            str: result from function create_local_data_base() from user_input module
        """
        return self.user_obj.create_local_data_base(table_names)

    def delete_local_db_rows(self, table_name: str, input_data: str):
        """calls delete_local_db_data() from user_input module to delete row with given input_data from given table_name

        Args:
            table_name (str): name of table to delete row from
            input_data (str): data to match and find the row

        Returns:
            str: result from function delete_local_db_data() from user_input module
        """
        return self.user_obj.delete_local_db_data(table_name, input_data)


class Java:
    implements = ['py4j.binary.SpeechApp']


class PythonJavaBridge(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    @staticmethod
    def send_python_obj_java_call():
        """Sends python object to the Java side.

        Raises:
            SpeechInvalidArgumentError: _description_

        Returns:
            str: SUCCESS if function works
                 FALIURE if function fails
        """
        try:
            _obj = PythonSpeechWrapper()
            # "Sends" python object to the Java side.
            result = speech_process.send_python_obj_to_java(_obj)
            if result == 0:
                logging.error("Failed to send python object to Java")
                return enums.FAILURE.name
            return enums.SUCCESS.name
        except Exception as e:
            raise SpeechInvalidArgumentError(e)

    @staticmethod
    def request_user_input_from_java(incomplete_input: list):
        """send incomplete_input to java side functions

        Args:
            incomplete_input (list): list from validate_user_input() function from retail_actions module

        Raises:
            SpeechProcessError: _description_

        Returns:
            str: SUCCESS if java side functions return something
                 FAILURE if java side functions return nothing
        """
        try:
            result = speech_process.fill_data_for_speech_request(incomplete_input)
            if result is None:
                logging.error("Failed to get requested input")
                return enums.FAILURE.name
            return enums.SUCCESS.name
        except Exception as e:
            raise SpeechProcessError(e)

    @staticmethod
    def update_new_words_to_analysis(new_user_words: list):
        """send the new word to java functions for update and analysis

        Args:
            new_user_words (list): list of words and its related description from user

        Raises:
            SpeechProcessError: _description_

        Returns:
            str: SUCCESS if java side functions return something
                 FAILURE if java side functions return nothing
        """
        try:
            result = speech_process.update_new_words_cloud(new_user_words)
            if result:
                logging.error("Failed to get requested input")
                return enums.FAILURE.name
            return enums.SUCCESS.name
        except Exception as e:
            raise SpeechProcessError(e)

    @staticmethod
    def process_user_intention_actions(words: list):
        """send words to java side functions

        Args:
            words (list): list containing all information about the word user entered

        Raises:
            SpeechProcessError: _description_
        """
        try:
            speech_process.process_user_actions(words)
        except Exception as e:
            raise SpeechProcessError(e)


# if __name__ == "__main__":
#     start_time_ = datetime.now()
#     obj = PythonSpeechWrapper()
#     obj.get_user_input("text", "what is this for")
#     print("Total execution time : %s " % (datetime.now() - start_time_))