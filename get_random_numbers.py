import random
import os
import time

number_of_results = 5
sleep_time_seconds = 10
number_of_frames = input("Enter the number of frames: ")

random_results = [random.randint(0, int(number_of_frames)) for _ in range(number_of_results)]

print(f"Generated ramdon numbers: {random_results}")

directory = input("Enter the directory path: ").strip()

for number in random_results:
    base_file_name = f"frame{number}.jpg"
    used_file_name = f"frame{number}_used.jpg"

    base_file_path = os.path.join(directory, base_file_name)
    used_file_path = os.path.join(directory, used_file_name)

    #Check if the directory exists
    if os.path.exists(base_file_path):
        #Open the file
        print(f"Opening {base_file_name}")
        os.startfile(base_file_path)
        
        print("Sleeping")
        time.sleep(sleep_time_seconds)


        new_file_name = f"frame{number}_used.jpg"
        new_file_path = os.path.join(directory, new_file_name)
        os.rename(base_file_path, new_file_path)

        

        print(f"Renamed {base_file_name} -> {new_file_name}")

    elif os.path.exists(used_file_path):
        #Just open the path if it already exists, no need to rename it
        print(f"File {used_file_name} already renamed, opening it")
        os.startfile(used_file_path)

        print("Sleeping")
        time.sleep(sleep_time_seconds)
    else:
        #Default error case
        print(f"No file found for frame{number} in the directory")

print("Exiting")