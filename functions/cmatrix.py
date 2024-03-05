import os
import subprocess
import threading
import time
import platform


def wait_for_enter():
    input("Press Enter to exit...")
    exit_flag.set()


def run_cmatrix_for_seconds(seconds):
    cmatrix_proc = subprocess.Popen(['cmatrix'])
    time.sleep(seconds)
    cmatrix_proc.terminate()
    cmatrix_proc.wait()


# Set a flag to signal script termination
exit_flag = threading.Event()

# Start a thread that waits for Enter press
input_thread = threading.Thread(target=wait_for_enter)
input_thread.start()

# Keep the script running until Enter is pressed or 15 minutes have passed
timeout = 900  # 15 minutes in seconds
start_time = time.time()

while not exit_flag.is_set():
    if time.time() - start_time > timeout:
        print("15 minutes have passed, exiting the script.")
        break
    time.sleep(1)  # Sleep to reduce CPU usage

run_cmatrix_for_seconds(5)

# Attempt to close the terminal window (may not work in all environments)
if platform.system() == "Windows":
    os.system('cls')  # For Windows
else:
    os.system('clear')  # For Unix-like systems (Linux, macOS)
print("Process finished, you can close the window now...")
