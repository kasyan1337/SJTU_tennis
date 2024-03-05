from datetime import datetime, timedelta
import os
import subprocess
import threading
import time
import pytz


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def run_ascii_aquarium_until_1157():
    def run_ascii_aquarium():
        return subprocess.Popen(['asciiquarium'])  # Assuming asciiquarium is in the PATH

    def check_time(beijing, aquarium_proc):
        while True:
            now = datetime.now(beijing)
            if now.hour == 12 and now.minute >= 29:
                aquarium_proc.terminate()
                aquarium_proc.wait()
                clear_screen()
                break
            time.sleep(60)  # Check the time every minute

    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    beijing = pytz.timezone('Asia/Shanghai')

    aquarium_proc = run_ascii_aquarium()
    time_check_thread = threading.Thread(target=check_time, args=(beijing, aquarium_proc))
    time_check_thread.start()
    time_check_thread.join()


# You can call this function directly for testing
run_ascii_aquarium_until_1157()
clear_screen()
