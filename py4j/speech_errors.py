import enum
import logging


class SpeechError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class SpeechProcessError(SpeechError):
    pass


class SpeechTimeOutError(SpeechError):
    pass


class SpeechInvalidArgumentError(SpeechError):
    pass


class SpeechResult(enum.Enum):
    SUCCESS = 0
    FAILURE = 1
    WARNING = 2
    INSUFFICIENT_INPUT = 3
    RETAILER_NOT_REGISTERED = 101
    ITEM_NOT_AVAILABLE = 102
    ADD_ONS_NOT_AVAILABLE = 103
    REQUEST_NOT_SATISFIED = 104
    REQUESTED_SERVICE_NOT_AVAILABLE = 105
    ITEM_OUT_OF_STOCK = 106
    INVALID_INPUT = 107
    INVALID_LOCATION = 108
    INVALID_ANDROID_ACTION_TYPE = 109

    FATAL_ERROR = -101
    DB_READ_ERROR = -102
    DB_DELETE_ERROR = -103
    DB_WRITE_ERROR = -104
    CONNECTION_ERROR = -105
    MODULE_NOT_RESPONDING = -106
    SERVICE_NOT_AVAILABLE = -107

    @staticmethod
    def get_error_description(error_num):
        try:
            logging.debug("Error type associated with error number {0} is : {1}".format(error_num,
                                                                                        SpeechResult(error_num)))
        except KeyError:
            raise SpeechInvalidArgumentError("Invalid error value")
