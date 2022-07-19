"""import cv2
import numpy as np
from PIL import Image
import os, time
import logging
import json
from datetime import datetime"""
import logging
from speech_errors import SpeechResult as enums
from speech_errors import SpeechProcessError, SpeechInvalidArgumentError
import user_database
import user_input

"""elif self.check_registered_retailer(is_android_action) is not None:
    retailer = is_android_action
    query_type = "order"
    return True"""

query_type = ""
business_name = ""
item_list = []
add_ons = []
description = []
action_type = ""
location = "hillsboro"

g_db_obj = user_database.ProcessDataBaseRequests()


class RetailActions:
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

    def get_retail_db_words(self, table, index):
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

    def validate_user_input(self, index):
        incomplete = self.is_input_incomplete(index)
        word = []
        if incomplete is not None:
            for item in incomplete:
                word.append(item)
            return word
        return None

    def is_input_incomplete(self, index):
        global query_type, business_name, item_list, add_ons, description
        result = []
        if query_type is None:
            result.append("query_type")
        if business_name is None:
            result.append("business_name")
        if not item_list:
            result.append("item_list")
        if item_list and not add_ons:
            if self.check_add_ons_need(index):
                result.append("add_ons")
            if self.check_description_need(index):
                result.append("description")
        if not result:
            return result
        return None

    def check_add_ons_need(self, index):
        try:
            addon_req = self.get_retail_db_words("Supply_Add_ons", index)
            if addon_req is not None:
                return addon_req
            return None
        except Exception as e:
            raise SpeechProcessError(e)

    def check_description_need(self, index):
        try:
            desc_need = self.get_retail_db_words("Supply_Descriptions", index)
            if desc_need is not None:
                return desc_need
            return None
        except Exception as e:
            raise SpeechProcessError(e)

    @staticmethod
    def generate_retail_action_request():
        lis = [{"query_type": query_type}, {"item_list": item_list},
               {"description": description}, {"business_name": business_name},
               {"add_ons": add_ons}]
        return lis

    def ret_get_more_input(self, incomplete):
        try:
            if self.g_ui_obj.request_user_for_input(incomplete) == enums.FAILURE.name:
                logging.error("Insufficient input from user, could not process the request '{}'".format(incomplete))
                self.g_ui_obj.update_user_input_to_cloud(incomplete)
                return enums.FAILURE.name
            return enums.SUCCESS.name
        except Exception as e:
            raise SpeechInvalidArgumentError(e)

    def get_business_name(self, index):
        try:
            self.get_retail_db_words("Businesses", index)
            if not self.words:
                logging.debug("No business in user request")
                return None
            else:
                if len(self.words) == 1:
                    return self.words[0]
                else:
                    logging.debug("Notify user and get confirmation")
        except Exception as e:
            raise SpeechProcessError(e)

    def get_business_action(self, index):
        try:
            self.get_retail_db_words("Business_actions", index)
            if not self.words:
                logging.debug("No business in user request")
                return None
            else:
                return self.words[0]
        except Exception as e:
            raise SpeechProcessError(e)

    def get_business_supplies_list(self, index):
        try:
            global business_name
            if business_name is not None:
                self.get_retail_db_words(business_name.decode("utf_8")+"_supplies", index)
            else:
                self.get_retail_db_words("Available_supplies", index)
            if not self.words:
                logging.debug("No business in user request")
                return None
            else:
                return self.words
        except Exception as e:
            raise SpeechProcessError(e)

    def check_retail_command_status(self, index):
        try:
            global business_name
            global item_list
            business_name = self.get_business_name(index)
            if business_name is not None:
                self.words.clear()
                item_list = self.get_business_supplies_list(index)
                if item_list is not None:
                    self.words.clear()
            else:
                item_list = self.get_business_supplies_list(index)
                if item_list is not None:
                    self.words.clear()
            global query_type
            query_type = self.get_business_action(index)
            if query_type is not None:
                self.words.clear()
            global description
            description = self.check_description_need(index)
            if description is not None:
                self.words.clear()
            global add_ons
            add_ons = self.check_add_ons_need(index)
            if add_ons is not None:
                self.words.clear()
        except Exception as e:
            raise SpeechProcessError(e)

    def decode_user_input_for_retail_actions(self, index, q_t):
        try:
            if index == 1 and self.get_retail_actions(self.get_retail_db_words("Business_actions", index)):
                logging.warning("This is of intention to " + query_type + " business action and incomplete")
                """ Request for user input"""
                words = self.validate_user_input(index)
                if self.ret_get_more_input(words) == enums.SUCCESS.name:
                    if self.check_retail_command_status(index) == enums.SUCCESS.name:
                        if self.validate_user_input(index) is not None:
                            q_t.put(enums.SUCCESS.name)
                        else:
                            q_t.put(enums.FAILURE.name)
                    else:
                        q_t.put(enums.FAILURE.name)
                else:
                    q_t.put(enums.FAILURE.name)
            else:
                if self.check_retail_command_status(index) == enums.SUCCESS.name:
                    words = self.validate_user_input(index)
                    if self.ret_get_more_input(words) == enums.SUCCESS.name:
                        if self.check_retail_command_status(index) == enums.SUCCESS.name:
                            if self.validate_user_input(index) is not None:
                                q_t.put(enums.SUCCESS.name)
                            else:
                                q_t.put(enums.FAILURE.name)
                        else:
                            q_t.put(enums.FAILURE.name)
                    else:
                        q_t.put(enums.FAILURE.name)
        except Exception as e:
            raise SpeechProcessError(e)

    def get_retail_actions(self, words):
        try:
            if words == self.data[0][2]:
                global query_type
                query_type = words.decode("utf_8")
                return words
            return None
        except Exception as e:
            raise SpeechProcessError(e)
