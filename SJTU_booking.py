#!/usr/bin/env python3

import base64
import configparser
import getpass
import logging
import os
import platform
import re
import subprocess
import threading
import time
from datetime import datetime, timedelta

import pytesseract
import requests
from PIL import Image
from colorama import init, Fore, Style
from playwright.sync_api import Playwright, sync_playwright, TimeoutError
from pytz import timezone

init()
#       ############################### SETUP ###############################

chosen_timeout = 200  # Timeout for waiting for element to appear (booking page)
random_timeout = 0.5  # Random timeout for waiting between actions
timeout_booking_page = 0.1  # Timeout for waiting between actions on the booking page
refresh_booking_page_at = 300000  # Refresh the booking page at this time (microseconds)

#      ############################### USER SETTINGS ###############################
cutoff_time = 0  # Time restriction for booking (1 for ON)
updater = 0  # Update the script from GitHub (1 for ON)

#       ############################### DATABASE ###############################

timeslots_tennis = {8: "div:nth-child(3) > .seat > .inner-seat > div",
                    9: "div:nth-child(4) > .seat > .inner-seat > div",
                    10: "div:nth-child(5) > .seat > .inner-seat > div",
                    11: "div:nth-child(6) > .seat > .inner-seat > div",
                    12: "div:nth-child(7) > .seat > .inner-seat > div",
                    13: "div:nth-child(8) > .seat > .inner-seat > div",
                    14: "div:nth-child(9) > .seat > .inner-seat > div",
                    15: "div:nth-child(10) > .seat > .inner-seat > div",
                    16: "div:nth-child(11) > .seat > .inner-seat > div",
                    17: "div:nth-child(12) > .seat > .inner-seat > div",
                    18: "div:nth-child(13) > .seat > .inner-seat > div",
                    19: "div:nth-child(14) > .seat > .inner-seat > div",
                    20: "div:nth-child(15) > .seat > .inner-seat > div",
                    21: "div:nth-child(16) > .seat > .inner-seat > div"}

seven_badminton = []

timeslots_badminton = {}

timeslots_badminton_1 = {8: "div:nth-child(3) > div > .inner-seat > div > img",
                         9: "div:nth-child(3) > div > .inner-seat > div > img",
                         10: "div:nth-child(3) > div > .inner-seat > div > img",
                         11: "div:nth-child(3) > div > .inner-seat > div > img",
                         12: "div:nth-child(3) > div > .inner-seat > div > img",
                         13: "div:nth-child(3) > div > .inner-seat > div > img",
                         14: "div:nth-child(3) > div > .inner-seat > div > img",
                         15: "div:nth-child(3) > div > .inner-seat > div > img",
                         16: "div:nth-child(3) > div > .inner-seat > div > img",
                         17: "div:nth-child(3) > div > .inner-seat > div > img",
                         18: "div:nth-child(3) > div > .inner-seat > div > img",
                         19: "div:nth-child(3) > div > .inner-seat > div > img",
                         20: "div:nth-child(3) > div > .inner-seat > div > img",
                         21: "div:nth-child(3) > div > .inner-seat > div > img"}

timeslots_badminton_2 = {8: "div:nth-child(3) > div:nth-child(2) > .inner-seat > div > img",
                         9: "div:nth-child(4) > div:nth-child(2) > .inner-seat > div > img",
                         10: "div:nth-child(5) > div:nth-child(2) > .inner-seat > div > img",
                         11: "div:nth-child(6) > div:nth-child(2) > .inner-seat > div > img",
                         12: "div:nth-child(7) > div:nth-child(2) > .inner-seat > div > img",
                         13: "div:nth-child(8) > div:nth-child(2) > .inner-seat > div > img",
                         14: "div:nth-child(9) > div:nth-child(2) > .inner-seat > div > img",
                         15: "div:nth-child(10) > div:nth-child(2) > .inner-seat > div > img",
                         16: "div:nth-child(11) > div:nth-child(2) > .inner-seat > div > img",
                         17: "div:nth-child(12) > div:nth-child(2) > .inner-seat > div > img",
                         18: "div:nth-child(13) > div:nth-child(2) > .inner-seat > div > img",
                         19: "div:nth-child(14) > div:nth-child(2) > .inner-seat > div > img",
                         20: "div:nth-child(15) > div:nth-child(2) > .inner-seat > div > img",
                         21: "div:nth-child(16) > div:nth-child(2) > .inner-seat > div > img"}

timeslots_badminton_3 = {8: "div:nth-child(3) > div:nth-child(3) > .inner-seat > div > img",
                         9: "div:nth-child(4) > div:nth-child(3) > .inner-seat > div > img",
                         10: "div:nth-child(5) > div:nth-child(3) > .inner-seat > div > img",
                         11: "div:nth-child(6) > div:nth-child(3) > .inner-seat > div > img",
                         12: "div:nth-child(7) > div:nth-child(3) > .inner-seat > div > img",
                         13: "div:nth-child(8) > div:nth-child(3) > .inner-seat > div > img",
                         14: "div:nth-child(9) > div:nth-child(3) > .inner-seat > div > img",
                         15: "div:nth-child(10) > div:nth-child(3) > .inner-seat > div > img",
                         16: "div:nth-child(11) > div:nth-child(3) > .inner-seat > div > img",
                         17: "div:nth-child(12) > div:nth-child(3) > .inner-seat > div > img",
                         18: "div:nth-child(13) > div:nth-child(3) > .inner-seat > div > img",
                         19: "div:nth-child(14) > div:nth-child(3) > .inner-seat > div > img",
                         20: "div:nth-child(15) > div:nth-child(3) > .inner-seat > div > img",
                         21: "div:nth-child(16) > div:nth-child(3) > .inner-seat > div > img"}

timeslots_badminton_4 = {8: "div:nth-child(3) > div:nth-child(4) > .inner-seat > div > img",
                         9: "div:nth-child(4) > div:nth-child(4) > .inner-seat > div > img",
                         10: "div:nth-child(5) > div:nth-child(4) > .inner-seat > div > img",
                         11: "div:nth-child(6) > div:nth-child(4) > .inner-seat > div > img",
                         12: "div:nth-child(7) > div:nth-child(4) > .inner-seat > div > img",
                         13: "div:nth-child(8) > div:nth-child(4) > .inner-seat > div > img",
                         14: "div:nth-child(9) > div:nth-child(4) > .inner-seat > div > img",
                         15: "div:nth-child(10) > div:nth-child(4) > .inner-seat > div > img",
                         16: "div:nth-child(11) > div:nth-child(4) > .inner-seat > div > img",
                         17: "div:nth-child(12) > div:nth-child(4) > .inner-seat > div > img",
                         18: "div:nth-child(13) > div:nth-child(4) > .inner-seat > div > img",
                         19: "div:nth-child(14) > div:nth-child(4) > .inner-seat > div > img",
                         20: "div:nth-child(15) > div:nth-child(4) > .inner-seat > div > img",
                         21: "div:nth-child(16) > div:nth-child(4) > .inner-seat > div > img"}

animations_not_installed_macos = ['wailanisangue']

beijing = timezone('Asia/Shanghai')
animations = None


#       ############################### CORE FUNCTIONS ###############################

def booking_crontab():
    """
    Decides whether to start manually or automatically based on config
    """
    global auto_launch, auto_captcha

    booking_off_crontab_config = config_parser()[7]
    if booking_off_crontab_config == 'OFF' or booking_off_crontab_config == 'off':
        quit()

    how_to_start_config = config_parser()[6]
    auto_launch = int(how_to_start_config)
    auto_captcha = int(how_to_start_config)


def start_logs():
    """
    Start logging to a file in the 'booking_logs' directory.
    """
    log_directory = "booking_logs"
    script_name_without_extension = os.path.splitext(os.path.basename(__file__))[0]
    script_path = __file__  # Gets the whole path of the current script
    log_filename = f"{script_name_without_extension}_log.log"
    log_path = os.path.join(log_directory, log_filename)

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Get the last modification time of the file
    last_modified_timestamp = os.path.getmtime(script_path)
    last_modified_time = datetime.fromtimestamp(last_modified_timestamp).strftime('%H-%M-%S %d-%m-%Y')

    logging.basicConfig(filename=log_path, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')

    logging.info(f"\n\n\n{'=' * 30}\nNew session started at "
                 f"{datetime.now(beijing).strftime('%H-%M-%S %d-%m-%Y')}\n{'=' * 30}\n"
                 f"Script last modified: {last_modified_time}\n"
                 f"Setup:\n"
                 f"chosen_timeout {chosen_timeout} ms\n"
                 f"random_timeout {random_timeout} s\n"
                 f"timeout_booking_page {timeout_booking_page} s\n"
                 f"refresh_booking_page_at {refresh_booking_page_at} microseconds\n"
                 f"auto_launch {auto_launch}\n"
                 f"time_restriction {cutoff_time}\n"
                 f"updater {updater}\n{'=' * 30}\n\n")


def extract_latency_logs(source_log_file, output_log_file):
    """
    Extracts latencies from a log file and writes them to a new file.
    """
    latency_pattern = re.compile(r'latency: (\d+\.\d+) seconds')
    setup_pattern = re.compile(
        r'Script last modified|Setup:|chosen_timeout|random_timeout|'
        r'timeout_booking_page|auto_captcha|time_restriction_hour|updater')
    user_pattern = re.compile(r'selected timeslot|OS:|Animations:')
    error_pattern = re.compile(r'ERROR -')
    executed_successfully_pattern = re.compile(r'EXECUTED SUCCESSFULLY: 提交订单')
    session_start_pattern = re.compile(r"New session started at")

    last_executed_successfully = None
    session_successful = False
    first_session = True

    with open(source_log_file, 'r') as source:
        lines_to_write = []

        for line in source:
            if session_start_pattern.search(line):
                if not first_session:
                    success_status = "Successfully submitted!" if session_successful else "Submission failed!"
                    lines_to_write.append(f"Session Status: {success_status}\n")
                    lines_to_write.append('=' * 30 + '\n')
                session_start_time = line.split()[-1]
                lines_to_write.append('=' * 30 + '\n')
                lines_to_write.append(f"Session started at {session_start_time}\n")
                first_session = False
                session_successful = False
            elif setup_pattern.search(line) or user_pattern.search(line) or "seconds" in line:
                lines_to_write.append(line)
            elif latency_pattern.search(line):
                match = latency_pattern.search(line)
                if match:
                    latency = match.group(1)
                    lines_to_write.append(f"{line.strip()} - Extracted Latency: {latency} seconds\n")
            elif executed_successfully_pattern.search(line):
                session_successful = True
                lines_to_write.append(line)
            elif error_pattern.search(line):
                if last_executed_successfully:
                    lines_to_write.append(last_executed_successfully)
                lines_to_write.append(line)
                last_executed_successfully = None

        if not first_session:
            success_status = "Successfully submitted!" if session_successful else "Submission failed!"
            lines_to_write.append(f"Session Status: {success_status}\n")
            lines_to_write.append('=' * 30 + '\n')

        with open(output_log_file, 'w') as output:
            for line in lines_to_write:
                output.write(line)


def config_parser():
    """
    Parses the config.ini file for the user's credentials.
    Not used just an example.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')

    username_config = config['credentials']['username']
    user_password_config = config['credentials']['password']
    timeslot_config = config['credentials']['timeslot']
    badminton_court_config = config['credentials']['badminton_court']
    animations_config = config['credentials']['animations']
    tennis_or_badminton_config = config['credentials']['tennis_or_badminton']
    read_config = config['credentials']['read_config']
    booking_off_crontab_config = config['credentials']['booking_crontab']
    # Not used; just notes of another method
    # username_zsh = os.getenv('SJTU_USERNAME')
    # user_password_zsh = os.getenv('SJTU_USER_PASSWORD')

    return (username_config, user_password_config, timeslot_config, badminton_court_config, animations_config,
            tennis_or_badminton_config, read_config, booking_off_crontab_config)


def update_file_from_github(file_name):
    """
    Automatically updates the specified file by downloading its latest version from GitHub.
    :param file_name: Name of the file to update (assuming it's in the root of the repository).
    """
    # GitHub raw content base URL
    base_url = "https://raw.githubusercontent.com/kasyan1337/SJTU_tennis/master/"
    url = f"{base_url}{file_name}"

    try:
        # Fetch the file content from GitHub
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Write the fetched content to the local file, overwriting it
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"File {file_name} is up to date.")
        logging.info(f"File {file_name} is up to date with the latest GitHub version.")
    except requests.RequestException as e:
        print(f"Failed to update {file_name}: {e}")
        logging.error(f"Failed to update {file_name} from GitHub: {e}")


def find_os():
    """
    Finds the operating system of the user for animation purposes.
    """
    if os.name == 'nt':
        return 'Windows'
    elif os.name == 'posix':
        if platform.system() == 'Darwin':
            return 'MacOS'
        elif platform.system() == 'Linux':
            return 'Linux'
        else:
            return 'Other POSIX'
    else:
        return 'Unknown'


def ocr_core(filename):
    text = pytesseract.image_to_string(Image.open(filename))
    return text


def run_cmatrix_for_seconds(seconds):
    """
    Runs cmatrix for a specified number of seconds. Checks if cmatrix is installed before running.
    """
    try:
        cmatrix_proc = subprocess.Popen(['cmatrix'])  # Try to start cmatrix
        time.sleep(seconds)  # Let it run for the specified number of seconds
        cmatrix_proc.terminate()  # Terminate the process
        cmatrix_proc.wait()  # Wait for process to terminate completely
    except FileNotFoundError:
        print("cmatrix not found. Please ensure it is installed and in the PATH.")


def clear_screen():
    """
    Clears the screen based on the user's operating system.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def run_ascii_aquarium():
    """
    Attempts to start the asciiquarium program and returns the process if successful.
    Returns None if asciiquarium is not installed.
    """
    try:
        return subprocess.Popen(['asciiquarium'])  # Ensure asciiquarium is installed and in the PATH
    except FileNotFoundError:
        print("asciiquarium not found. Please ensure it is installed and in the PATH.")
        return None


def check_time_1157(beijing, aquarium_proc):
    """
    Monitors the time and terminates the asciiquarium process at 11:57 AM.
    """
    while True:
        now = datetime.now(beijing)
        if now.hour == 11 and now.minute >= 57:
            if aquarium_proc:
                aquarium_proc.terminate()
                aquarium_proc.wait()
            clear_screen()
            break
        time.sleep(60)  # Check the time every minute


def run_ascii_aquarium_until_1157():
    """
    Runs asciiquarium until 11:57 AM, then terminates it. Ensures that asciiquarium
    is only running during the specified time window.
    """
    aquarium_proc = run_ascii_aquarium()
    if aquarium_proc is not None:
        time_check_thread = threading.Thread(target=check_time_1157, args=(beijing, aquarium_proc))
        time_check_thread.start()
        time_check_thread.join()


def intro():
    """
    Prints the introduction message.
    """
    current_datetime = datetime.now(beijing)
    # Calculate the date 7 days from now
    future_date = current_datetime + timedelta(days=7)

    # Format the date as "Weekday, Month day, Year"
    future_date_formatted = future_date.strftime("%A, %B %d, %Y")

    print(f"\033[1m\033[94mSJTU BOOKING ASSISTANT BY kasyan98\033[0m\n\n"
          f"You are booking a court for \033[43m{future_date_formatted}\033[0m")


def cutoff_time_else_intro():
    """
    Exits the script if past cutoff time
    """
    current_datetime = datetime.now(beijing)
    cutoff_time = current_datetime.replace(hour=12, minute=15, second=0, microsecond=0)
    # Check if the current time is past the cutoff time
    if current_datetime > cutoff_time:
        print("It is already past 12:15PM. You should try again tomorrow before 12:00.")
        time.sleep(5)
        quit()
    else:
        intro()


def end_at_enter():
    """
    After booking ends the script with enter
    """

    def wait_for_enter():
        input("Press Enter to exit...")
        exit_flag.set()

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
        time.sleep(10)  # Sleep to reduce CPU usage


def countdown_new():
    # Countdown to 12:00:00
    while True:
        now = datetime.now(beijing)
        if now.hour == 11:
            if now.minute < 58:
                # Refresh every minute before 11:58
                request_time_formatted = now.strftime("%H:%M:%S")
                print(f"{request_time_formatted} Waiting for the right time, refreshing every minute...")
                time.sleep(60)
            elif 58 <= now.minute < 59 and now.second <= 30:
                # Refresh every 10 seconds between 11:58 and 11:59:30
                request_time_formatted = now.strftime("%H:%M:%S")
                print(f"{request_time_formatted} Getting closer, refreshing every 10 seconds...")
                time.sleep(10)
            elif now.minute == 59 and now.second < 50:
                # Refresh every second from 11:59:30 to 11:59:50
                request_time_formatted = now.strftime("%H:%M:%S")
                print(f"{request_time_formatted} Almost there, refreshing every second...")
                time.sleep(1)
            elif now.minute == 59 and now.second >= 50:
                # Start the countdown at 11:59:50
                if now.second == 50:
                    for remaining in range(10, 1, -1):  # from 10 to 2 included
                        print(f"\033[1mCountdown: {remaining} seconds left until 12:00:00\033[0m")
                        time.sleep(1)

                # More precise timing starting from 11:59:50
                target_time = now.replace(second=59,
                                          microsecond=refresh_booking_page_at)
                while datetime.now(beijing) < target_time:
                    time.sleep(0.01)  # Sleep in small intervals to check more frequently
                print("\033[1mCountdown: 1 second left until 12:00:00\033[0m")
                break
        else:
            # Refresh every minute before 11:00
            request_time_formatted = now.strftime("%H:%M:%S")
            print(f"{request_time_formatted} Waiting for the right time, refreshing every minute...")
            time.sleep(60)


def ask_t_or_b():
    global chosen_sport
    tennis_or_badminton_input = input("Please enter 'T' for tennis or 'B' for badminton: ")

    if tennis_or_badminton_input == 'b' or tennis_or_badminton_input == 'B':
        chosen_sport = 'badminton'
        logging.info("USER SELECTED BADMINTON")
    elif tennis_or_badminton_input == 't' or tennis_or_badminton_input == 'T':
        logging.info("USER SELECTED TENNIS")
    else:
        print("Invalid input. Please try again.")
        logging.error(f"User input error: {tennis_or_badminton_input}. Exiting script.")
        time.sleep(5)
        quit()
    return chosen_sport


def timeslot_format_testing(chosen_timeslot):
    while True:
        # Check if input is all digits
        if chosen_timeslot.isdigit():
            # Convert to integer
            chosen_timeslot_int = int(chosen_timeslot)
            # Check if the integer is in the timeslots keys
            if 7 <= chosen_timeslot_int <= 21:
                break  # Exit the loop if valid timeslot
            else:
                print(Fore.RED + "The timeslot is not available." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Input is not a valid number." + Style.RESET_ALL)

        # Prompt again if not valid or not available
        chosen_timeslot = input(
            'Please enter your desired time slot \033[1min format "8,9,10...19,20,21".\033[0m\n'
            'Input has to be a number from the available slots:\n')
    return chosen_timeslot_int


def auto_captcha_function(page):
    page.wait_for_selector('img#captcha-img')
    logging.info("CAPTCHA: img#captcha-img")

    # Get the Data URI of the captcha image
    image_data_uri = page.evaluate("""() => {
            const img = document.querySelector('img#captcha-img');
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;
            ctx.drawImage(img, 0, 0);
            return canvas.toDataURL('image/jpeg');
        }""")

    # Extract base64 data from URI
    base64_data = image_data_uri.split(',')[1]
    image_data = base64.b64decode(base64_data)
    logging.info("CAPTCHA: Extracted base64 data from URI")

    # Save the captcha image
    image_path = 'captcha.jpg'
    with open(image_path, 'wb') as image_file:
        image_file.write(image_data)
    logging.info("CAPTCHA: Saved the captcha image")

    extracted_text = ocr_core(image_path)
    automatic_captcha = extracted_text
    logging.info(f"CAPTCHA: OCR performed successfully({extracted_text})")
    return automatic_captcha


def choosing_badminton_court(chosen_court):
    global timeslots_badminton
    while True:
        if chosen_court.isdigit():
            # Convert to integer
            chosen_court_int = int(chosen_court)
            if chosen_court_int in [1, 2, 3, 4]:
                if chosen_court_int == 1:
                    timeslots_badminton = timeslots_badminton_1
                    seven_badminton.append(".inner-seat > div > img")
                elif chosen_court_int == 2:
                    timeslots_badminton = timeslots_badminton_2
                    seven_badminton.append("div:nth-child(2) > .inner-seat > div > img")
                elif chosen_court_int == 3:
                    timeslots_badminton = timeslots_badminton_3
                    seven_badminton.append("div:nth-child(3) > .inner-seat > div > img")
                elif chosen_court_int == 4:
                    timeslots_badminton = timeslots_badminton_4
                    seven_badminton.append("div:nth-child(4) > .inner-seat > div > img")
                break
            else:
                print(Fore.RED + "The court is not available." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Input is not a valid number." + Style.RESET_ALL)
        # Prompt again if not valid or not available
        chosen_court = input('\033[1mPlease enter your preferred court number(format: "1,2,3,4"):\033[0m'
                             'Input has to be a number from the available courts:\n')
    return timeslots_badminton


def preparatory_stage(page, chosen_sport):
    logging.info(f"EXECUTED SUCCESSFULLY: Logged in")
    time.sleep(random_timeout)
    login_successful = True
    if login_successful and auto_captcha == 1:
        # Delete the captcha image after use
        os.remove('captcha.jpg')
        logging.info("CAPTCHA: Image deleted after successful login.")

    page.get_by_text("Service", exact=True).click()
    logging.info(f"EXECUTED SUCCESSFULLY: Service")
    time.sleep(random_timeout)
    page.locator("div").filter(has_text=re.compile(r"^Sport$")).nth(1).click()
    logging.info(f"EXECUTED SUCCESSFULLY: Clicked ^Sport$")
    time.sleep(random_timeout)
    with page.expect_popup() as page1_info:
        page.get_by_text("Sports Venue Booking标签：暂无评分 复制链接 收藏").click()
    page1 = page1_info.value
    logging.info(f"EXECUTED SUCCESSFULLY: Sports Venue Booking标签：暂无评分 复制链接 收藏")
    time.sleep(random_timeout)
    page1.get_by_placeholder("请输入场馆名称或活动类型名称").click()
    logging.info(f"EXECUTED SUCCESSFULLY: 请输入场馆名称或活动类型名称")
    time.sleep(random_timeout)

    # Different path on website
    if chosen_sport == 'badminton':
        page1.get_by_placeholder("请输入场馆名称或活动类型名称").fill("羽毛球")
        logging.info(f"EXECUTED SUCCESSFULLY: 羽毛球")
        time.sleep(random_timeout)
        page1.get_by_placeholder("请输入场馆名称或活动类型名称").press("Enter")
        logging.info(f"EXECUTED SUCCESSFULLY: Enter")
        time.sleep(random_timeout)

        page1.locator("li").filter(has_text="徐汇校区体育馆 地址：徐汇校区 时间：09:00-22:").get_by_role(
            "img").click()  # Xuhui

        time.sleep(random_timeout)
        logging.info(f"EXECUTED SUCCESSFULLY: 徐汇校区体育馆 地址：徐汇校区 时间：09:00-22:")
        page1.locator("#loginSelection").get_by_role("button", name="校内人员登录").click()
        time.sleep(random_timeout)
        logging.info(f"EXECUTED SUCCESSFULLY: 校内人员登录")
        page1.get_by_placeholder("请输入场馆名称或活动类型名称").click()
        time.sleep(random_timeout)
        logging.info(f"EXECUTED SUCCESSFULLY: 请输入场馆名称或活动类型名称")
        page1.get_by_placeholder("请输入场馆名称或活动类型名称").fill("羽毛球")
        time.sleep(random_timeout)
        logging.info(f"EXECUTED SUCCESSFULLY: 羽毛球")
        page1.get_by_placeholder("请输入场馆名称或活动类型名称").press("Enter")
        time.sleep(random_timeout)
        logging.info(f"EXECUTED SUCCESSFULLY: Enter")
        page1.locator("li").filter(has_text="徐汇校区体育馆 地址：徐汇校区 时间：09:00-22:").get_by_role(
            "img").click()  # Xuhui
        time.sleep(random_timeout)
        logging.info(f"EXECUTED SUCCESSFULLY: 徐汇校区网球场 地址：徐汇校区 时间：07:00-22:")
        page1.get_by_role("tab", name="羽毛球").click()
        time.sleep(random_timeout)
        logging.info(f"EXECUTED SUCCESSFULLY: TAB NAME: 羽毛球")
    else:
        page1.get_by_placeholder("请输入场馆名称或活动类型名称").fill("网球")
        logging.info(f"EXECUTED SUCCESSFULLY: 网球")
        time.sleep(random_timeout)
        page1.get_by_placeholder("请输入场馆名称或活动类型名称").press("Enter")
        logging.info(f"EXECUTED SUCCESSFULLY: Enter")
        time.sleep(random_timeout)

        # page1.locator("li").filter(has_text="胡晓明网球场 地址：闵行校区 时间：07:00-22:").get_by_role("img").click() # Minhang
        page1.locator("li").filter(has_text="徐汇校区网球场 地址：徐汇校区 时间：07:00-22:").get_by_role(
            "img").click()  # Xuhui
        time.sleep(random_timeout)
        logging.info(f"EXECUTED SUCCESSFULLY: 徐汇校区网球场 地址：徐汇校区 时间：07:00-22:")
        page1.locator("#loginSelection").get_by_role("button", name="校内人员登录").click()
        time.sleep(random_timeout)
        logging.info(f"EXECUTED SUCCESSFULLY: 校内人员登录")
        page1.get_by_placeholder("请输入场馆名称或活动类型名称").click()
        time.sleep(random_timeout)
        logging.info(f"EXECUTED SUCCESSFULLY: 请输入场馆名称或活动类型名称")
        page1.get_by_placeholder("请输入场馆名称或活动类型名称").fill("网球")
        time.sleep(random_timeout)
        logging.info(f"EXECUTED SUCCESSFULLY: 网球")
        page1.get_by_placeholder("请输入场馆名称或活动类型名称").press("Enter")
        time.sleep(random_timeout)
        logging.info(f"EXECUTED SUCCESSFULLY: Enter")
        # page1.locator("li").filter(has_text="胡晓明网球场 地址：闵行校区 时间：07:00-22:").get_by_role("img").click() # Minhang
        page1.locator("li").filter(has_text="徐汇校区网球场 地址：徐汇校区 时间：07:00-22:").get_by_role(
            "img").click()  # Xuhui
        time.sleep(random_timeout)
        logging.info(f"EXECUTED SUCCESSFULLY: 徐汇校区网球场 地址：徐汇校区 时间：07:00-22:")

    # Preparatory stage logs
    latency_part1_end = time.time()
    latency_part1_report = latency_part1_end - latency_part1_start
    print(f"Preparatory stage latency: {latency_part1_report:.2f} seconds")
    logging.info(f"Preparatory stage latency: {latency_part1_report:.2f} seconds")
    logging.info(f"PREPARATORY STAGE FINISHED; WAITING FOR 12:00")
    return page1


def final_stage(page1, latency_part2_start):
    latency_part2_end = time.time()
    latency_part2_report_end = latency_part2_end - latency_part2_start
    print(
        Fore.GREEN + f"\n\033[1mBooking completed at {datetime.now(beijing).strftime('%H:%M:%S:%f')} "
                     f"in {latency_part2_report_end:.2f} seconds!\033[0m" + Style.RESET_ALL)
    logging.info(
        f"Booking completed at {datetime.now(beijing).strftime('%H:%M:%S:%f')} "
        f"in {latency_part2_report_end:.2f} seconds!")
    logging.error("Script terminated due to an error.")

    extract_latency_logs('booking_logs/SJTU_booking_log.log', 'booking_logs/Stats.log')

    page1.get_by_role("button", name="立即支付").click()
    logging.info(f"EXECUTED SUCCESSFULLY: 立即支付")
    time.sleep(random_timeout)
    page1.get_by_role("button", name="确 定").click()
    logging.info(f"EXECUTED SUCCESSFULLY: 确 定")
    time.sleep(random_timeout)
    page1.get_by_role("button", name="yes").click(timeout=900000)  # Increased timeout
    logging.info(f"EXECUTED SUCCESSFULLY: yes")
    time.sleep(random_timeout)


def login_if_auto_launch_on(page, chosen_sport):
    global animations, timeslots_badminton
    username_config = config_parser()[0]
    user_password_config = config_parser()[1]
    timeslot_config = config_parser()[2]
    badminton_court_config = config_parser()[3]
    animations_config = config_parser()[4]
    tennis_or_badminton_config = config_parser()[5]
    if tennis_or_badminton_config == 'b' or tennis_or_badminton_config == 'B':
        chosen_sport = 'badminton'

    chosen_court = badminton_court_config
    # choosing the court
    if chosen_sport == 'badminton':
        while True:
            if chosen_court.isdigit():
                # Convert to integer
                chosen_court_int = int(chosen_court)
                if chosen_court_int in [1, 2, 3, 4]:
                    if chosen_court_int == 1:
                        timeslots_badminton = timeslots_badminton_1
                        seven_badminton.append(".inner-seat > div > img")
                    elif chosen_court_int == 2:
                        timeslots_badminton = timeslots_badminton_2
                        seven_badminton.append("div:nth-child(2) > .inner-seat > div > img")
                    elif chosen_court_int == 3:
                        timeslots_badminton = timeslots_badminton_3
                        seven_badminton.append("div:nth-child(3) > .inner-seat > div > img")
                    elif chosen_court_int == 4:
                        timeslots_badminton = timeslots_badminton_4
                        seven_badminton.append("div:nth-child(4) > .inner-seat > div > img")
                    break
                else:
                    print(Fore.RED + "The court is not available." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Input is not a valid number." + Style.RESET_ALL)
            # Prompt again if not valid or not available
            chosen_court = input('\033[1mPlease enter your preferred court number(format: "1,2,3,4"):\033[0m'
                                 'Input has to be a number from the available courts:\n')

    chosen_timeslot = timeslot_config
    # timeslot format test
    chosen_timeslot_int = timeslot_format_testing(chosen_timeslot)

    while True:
        # AUTOMATIC CAPTCHA
        if auto_captcha == 1:
            auto_captcha_function(page)

        automatic_captcha = auto_captcha_function(page)
        latency_part1_start = time.time()
        logging.info(f"{username_config} selected timeslot: {chosen_timeslot_int}")

        # Animation prompt
        logging.info(f"OS: {find_os()}")
        if find_os() == 'MacOS' and username_config not in animations_not_installed_macos:
            animations = animations_config
            logging.info(f"Animations: {animations}")

        # Fill in the login form
        page.get_by_placeholder("Account").click()
        page.get_by_placeholder("Account").fill(username_config)
        page.get_by_placeholder("Password").click()
        page.get_by_placeholder("Password").fill(user_password_config)
        page.get_by_placeholder("Captcha").click()
        if auto_captcha == 1:
            page.get_by_placeholder("Captcha").fill(automatic_captcha)
        else:
            page.get_by_placeholder("Captcha").fill(captcha_input)
        page.get_by_role("button", name="SIGN IN").click()
        # Cmatrix animation
        if animations == 'Y' or animations == 'y' and find_os() == 'MacOS':
            run_cmatrix_for_seconds(3)
            clear_screen()
            logging.info(f"EXECUTED SUCCESSFULLY: cmatrix animation")

        # Wait for response after login attempt
        page.wait_for_timeout(2000)  # Adjust timeout as needed

        # Check for login failure
        if page.is_visible("text=Wrong username or password") or page.is_visible("text=Wrong captcha"):
            if page.is_visible("text=Wrong captcha"):
                logging.info("CAPTCHA: WRONG CAPTCHA")
            print(Fore.RED + "Login failed. Please try again." + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "Login successful, proceeding..." + Style.RESET_ALL)
            break
    return (chosen_sport, latency_part1_start, chosen_timeslot_int, timeslots_badminton, timeslots_tennis,
            chosen_timeslot, animations, automatic_captcha)


def login_if_auto_launch_off(page, chosen_sport):
    global captcha_input, animations, latency_part1_start, chosen_timeslot_int, timeslots_badminton, timeslots_tennis, \
        chosen_timeslot, automatic_captcha
    if auto_launch != 1:
        # MANUAL SETUP
        chosen_sport = ask_t_or_b()

        if chosen_sport == 'badminton':
            chosen_court = input('\033[1mPlease enter your preferred court number(format: "1,2,3,4"):\033[0m')

            # choosing the court
            timeslots_badminton = choosing_badminton_court(chosen_court)

        chosen_timeslot = input('\033[1mPlease enter your desired time slot(format: "7,8,9,10...18,19,20,21"):\033[0m')
        # timeslot format test
        chosen_timeslot_int = timeslot_format_testing(chosen_timeslot)

        while True:
            # AUTOMATIC CAPTCHA
            if auto_captcha == 1:
                auto_captcha_function(page)

            automatic_captcha = auto_captcha_function(page)
            # INPUTS
            latency_part1_start = time.time()
            # Prompt the user for their account details
            account_input = input("\033[1mPlease enter your username: \033[0m")
            password_input = getpass.getpass("\033[1mPlease enter your password: \033[0m")
            if auto_captcha != 1:
                captcha_input = input("\033[1mPlease enter the captcha: \033[0m")
            logging.info(f"{account_input} selected timeslot: {chosen_timeslot_int}")
            # Animation prompt
            logging.info(f"OS: {find_os()}")
            if find_os() == 'MacOS' and account_input not in animations_not_installed_macos:
                animations = input("\033[1mWould you like to see animations while waiting? (Y/N): \033[0m")
                logging.info(f"Animations: {animations}")

            # Fill in the login form
            page.get_by_placeholder("Account").click()
            page.get_by_placeholder("Account").fill(account_input)
            page.get_by_placeholder("Password").click()
            page.get_by_placeholder("Password").fill(password_input)
            page.get_by_placeholder("Captcha").click()
            if auto_captcha == 1:
                page.get_by_placeholder("Captcha").fill(automatic_captcha)
            else:
                page.get_by_placeholder("Captcha").fill(captcha_input)
            page.get_by_role("button", name="SIGN IN").click()

            # Cmatrix animation
            if animations == 'Y' or animations == 'y' and find_os() == 'MacOS':
                run_cmatrix_for_seconds(3)
                clear_screen()
                logging.info(f"EXECUTED SUCCESSFULLY: cmatrix animation")

            # Wait for response after login attempt
            page.wait_for_timeout(2000)  # Adjust timeout as needed

            # Check for login failure
            if page.is_visible("text=Wrong username or password") or page.is_visible("text=Wrong captcha"):
                if page.is_visible("text=Wrong captcha"):
                    logging.info("CAPTCHA: WRONG CAPTCHA")
                print(Fore.RED + "Login failed. Please try again." + Style.RESET_ALL)
            else:
                print(Fore.GREEN + "Login successful, proceeding..." + Style.RESET_ALL)
                break
    return (chosen_sport, latency_part1_start, chosen_timeslot_int, timeslots_badminton, timeslots_tennis,
            chosen_timeslot, animations, automatic_captcha)


# Main function
def run_common(playwright: Playwright) -> None:
    global animations, timeslots_badminton, automatic_captcha, captcha_input, chosen_timeslot, latency_part1_start
    chosen_sport = 'Sport has not been chosen'

    # Check if the current time is past the cutoff time; or prints the intro
    if cutoff_time == 1:
        cutoff_time_else_intro()
    else:
        intro()

    # script start

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(record_video_dir="booking_logs")
    context.set_default_timeout(900000)  # Set default timeout to 15 mins
    page = context.new_page()
    page.goto(
        "https://my.sjtu.edu.cn/ui/me")
    logging.info(f"EXECUTED SUCCESSFULLY: Page accessed.")

    # Login
    if auto_launch == 1:
        unpack_data = login_if_auto_launch_on(page, chosen_sport)
    else:
        unpack_data = login_if_auto_launch_on(page, chosen_sport)

    # Unpack the data
    chosen_sport = unpack_data[0]
    latency_part1_start = unpack_data[1]
    chosen_timeslot_int = unpack_data[2]
    timeslots_badminton = unpack_data[3]
    timeslots_tennis = unpack_data[4]
    chosen_timeslot = unpack_data[5]
    animations = unpack_data[6]
    automatic_captcha = unpack_data[7]

    # After successful login to countdown
    page1 = preparatory_stage(page, chosen_sport)

    # Select 7 days from now variables
    current_date = datetime.now(beijing)
    next_week_date = current_date + timedelta(days=7)
    date_number = next_week_date.day
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday = weekdays[next_week_date.weekday()]

    # Aquarium animation
    if animations == 'Y' or animations == 'y' and find_os() == 'MacOS':
        run_ascii_aquarium_until_1157()
        clear_screen()
        logging.info(f"AQUARIUM ANIMATION FINISHED; WAITING FOR 12:00")

    # Countdown to 12:00:00
    countdown_new()

    #   ############################### AS FAST AS POSSIBLE FROM HERE ###############################
    latency_part2_start = time.time()
    element_clicked = False
    logging.info(f"EXECUTED SUCCESSFULLY: WAITED UNTIL 12:00")

    # Access the booking page
    while not element_clicked:
        page1.reload()
        if chosen_sport == 'badminton':
            page1.get_by_role("tab", name="羽毛球").click()  # MOVED HERE
            logging.info(f"EXECUTED SUCCESSFULLY: SWITCHED TO 羽毛球 TAB")

        try:
            # Wait for the element using wait_for_selector
            # page1.get_by_role("tab", name="羽毛球").click()  # maybe try without next time
            page1.wait_for_selector(f"text=月{date_number:02d}日 ({weekday})", timeout=chosen_timeout)
            page1.get_by_role("tab", name=f"月{date_number:02d}日 ({weekday})").click()
            print("\nSuccessfully accessed the booking page!")
            element_clicked = True
        except TimeoutError:
            # If wait_for_selector fails, check visibility
            if page1.is_visible(f"text=月{date_number:02d}日 ({weekday})"):
                # page1.get_by_role("tab", name="羽毛球").click()  # maybe try without next time
                page1.get_by_role("tab", name=f"月{date_number:02d}日 ({weekday})").click()
                print("\nSuccessfully clicked the booking tab!")
                element_clicked = True

        if element_clicked:
            latency_part2_mid = time.time()
            latency_part2_report_mid = latency_part2_mid - latency_part2_start
            print(Fore.GREEN +
                  f"Booking page accessed at {datetime.now(beijing).strftime('%H:%M:%S:%f')} "
                  f"in {latency_part2_report_mid:.2f} seconds"
                  + Style.RESET_ALL)
            logging.info(
                f"Booking page accessed at {datetime.now(beijing).strftime('%H:%M:%S:%f')} "
                f"in {latency_part2_report_mid:.2f} seconds")

        if not element_clicked:
            print(
                Fore.RED + f"Looking for 月{date_number:02d}日 ({weekday}) Element not found yet, retrying..."
                + Style.RESET_ALL)
            time.sleep(0.5)  # Brief pause before retrying

    # Timeslot selection
    if chosen_sport == 'badminton':
        if chosen_timeslot == '7':
            # time.sleep(timeout_booking_page) # temporarily disabling
            page1.locator(seven_badminton[0]).first.click()
            logging.info(f"EXECUTED SUCCESSFULLY: TIMESLOT 7 SELECTED")
        else:
            # time.sleep(timeout_booking_page) # temporarily disabling
            page1.locator(timeslots_badminton[int(chosen_timeslot)]).click()
            logging.info(f"EXECUTED SUCCESSFULLY: TIMESLOT {timeslots_badminton[int(chosen_timeslot)]} SELECTED")
    else:
        if chosen_timeslot == '7':
            # time.sleep(timeout_booking_page) # temporarily disabling
            page1.locator(".inner-seat > div").first.click()
            logging.info(f"EXECUTED SUCCESSFULLY: TIMESLOT 7 SELECTED")
        else:
            # time.sleep(timeout_booking_page) # temporarily disabling
            page1.locator(timeslots_tennis[int(chosen_timeslot)]).click()
            logging.info(f"EXECUTED SUCCESSFULLY: TIMESLOT {timeslots_tennis[int(chosen_timeslot)]} SELECTED")

    # Submitting order
    # time.sleep(timeout_booking_page) # maybe not needed here
    page1.get_by_role("button", name="立即下单").click()
    logging.info(f"EXECUTED SUCCESSFULLY: 立即下单")
    # time.sleep(timeout_booking_page) # temporarily disabling
    page1.locator("label span").nth(1).click()
    # time.sleep(timeout_booking_page) # maybe not needed here
    logging.info(f"EXECUTED SUCCESSFULLY: label span")
    # time.sleep(timeout_booking_page) # maybe not needed here
    page1.get_by_role("button", name="提交订单").click()

    #   ############################### AS FAST AS POSSIBLE TO HERE ###############################

    logging.info(f"EXECUTED SUCCESSFULLY: 提交订单")
    time.sleep(timeout_booking_page)

    # Here add alternative booking dates if error # TODO

    final_stage(page1, latency_part2_start)

    # Function to wait for Enter press
    end_at_enter()

    # ---------------------
    context.close()
    browser.close()
    # ---------------------


#       ############################### RUN ###############################

# Start automatically or manually based on config using crontab
booking_crontab()

# Starting logs
start_logs()

# Update or not
if updater == 1:
    script_name_with_extension = os.path.basename(__file__)
    update_file_from_github(script_name_with_extension)

# Run the script
try:
    with sync_playwright() as playwright:
        run_common(playwright)
    logging.info("Script successfully ended.")
except Exception as e:
    logging.exception(f"An unexpected error occurred: {e}")
