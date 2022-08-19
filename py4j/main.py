import user_database
import user_input
import android_actions
import retail_actions
import python_wrapper
import speech_errors
from time import time
import os

print(__name__)
print("before start")
if __name__ == "__main__":
    print("start")
    start_time_ = time()
    print(1)
    user_obj = user_input.ProcessUserInput()
    print(2)
    obj = python_wrapper.PythonSpeechWrapper()
    print(3)

    if "user_tasks.db" not in os.listdir(r"C:\Users\kc\website\checkinput"):
        read_file = user_obj.read_input_db_file("py4j/data.txt")
        obj.create_local_db_tables(table_names=user_input.table_names)
        user_input.table_names.clear(), user_input.android_input_data.clear(), user_input.business_input_data.clear(), user_input.supplies_input_data.clear(), user_input.data_tag.clear()

    # obj.update_local_db("py4j/data.txt")
    # user_text = input("enter something\n")
    ui = obj.get_user_input("text")
    # print(1)
    
    # print(2)
    print(ui)
    # dl = obj.delete_local_db_rows("supply_add_ons", "pizza")
    print("Total execution time : %s " %(time() - start_time_))


