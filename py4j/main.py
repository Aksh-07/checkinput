from msilib.schema import tables
import user_database
import user_input
import android_actions
import retail_actions
import python_wrapper
import speech_errors
from time import time

if __name__ == "__main__":
    start_time_ = time()
    # user_obj = user_input.ProcessUserInput()
    # read_file = user_obj.read_input_db_file("py4j/data.txt")
    # tables = user_input.table_names
    obj = python_wrapper.PythonSpeechWrapper()
    # obj.create_local_db_tables(table_names=tables)
    # obj.update_local_db("py4j/data.txt")
    ui = obj.get_user_input("text", "tshirt")
    print(ui)
    print("Total execution time : %s " %(time() - start_time_))


