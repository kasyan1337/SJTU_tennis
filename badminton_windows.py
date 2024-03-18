#!/usr/bin/env python3

import getpass
import os
import re
import threading
import time
from datetime import datetime, timedelta

from colorama import init, Fore, Style
from playwright.sync_api import Playwright, sync_playwright
from playwright.sync_api import TimeoutError
from pytz import timezone

init()

chosen_timeout = 200

# ### UPDATER ###
import requests


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
        print(f"{file_name} has been updated to the latest version.")
    except requests.RequestException as e:
        print(f"Failed to update {file_name}: {e}")


# Example usage:
file_name = "badminton_windows.py"
update_file_from_github(file_name)

# ### UPDATER ###

# First court
# page1.locator(".inner-seat > div > img").first.click()
# page1.locator("div:nth-child(3) > div > .inner-seat > div > img").first.click()
# page1.locator("div:nth-child(16) > div > .inner-seat > div > img").first.click()

# Court 4
# page1.locator("div:nth-child(4) > .inner-seat > div > img").first.click()  # 7AM

timeslots = {8: "div:nth-child(3) > div:nth-child(4) > .inner-seat > div > img",
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

beijing = timezone('Asia/Shanghai')


def run(playwright: Playwright) -> None:
    """
    This is a script that books a badminton court in SJTU Xuhui campus.
    Script navigates you to the booking page, then waits for 12:00:01(Beijing time), for the booking to open,
     then proceeds.
    Script supports booking only one week ahead, meaning if today is Monday 11:00AM, you're booking for next Monday.
    Otherwise, ur lazy ass can just do it on ur own without the script.
    Script is going to need x user inputs, if u accidentally make a mistake in any of them, close the whole thing
    and rerun the script.
    If you get an error message, send it together with hongbao to: WeChat ID: kasyan98
    Enjoy xoxo
    """

    # if past 12:15

    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    current_datetime = datetime.now(beijing)
    cutoff_time = current_datetime.replace(hour=12, minute=15, second=0, microsecond=0)
    # Check if the current time is past the cutoff time
    if current_datetime > cutoff_time:
        print("It is already past 12:15PM. You should try again tomorrow before 12:00.")
        time.sleep(5)
        quit()
    else:

        # Calculate the date 7 days from now
        future_date = current_datetime + timedelta(days=7)

        # Format the date as "Weekday, Month day, Year"
        future_date_formatted = future_date.strftime("%A, %B %d, %Y")

        # Use the formatted date in the print statement

        print(
            "THIS IS A SCRIPT THAT BOOKS A BADMINTON COURT ON SJTU XUHUI CAMPUS!\n\n"
            "The script navigates you to the booking page, then waits until 12:00:01(Beijing time) for the booking to"
            " open, then proceeds.\n"
            "The script supports booking\033[1m only one week ahead\033[0m, meaning if today is Monday 11:00AM, "
            "you're booking for next Monday.\n"
            "Otherwise ur lazy ass can just do it yourself without the script. \n"
            "If you get an error message, send it together with hongbao to:"
            " \033[1m\033[94m Wechat ID: kasyan98\033[0m and follow me on GitHub: https://github.com/kasyan1337\n\n"
            "Enjoy xoxo\n")

        print(f"You are booking the badminton court for \033[43m{future_date_formatted}\033[0m")

    # script start

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(
        "https://my.sjtu.edu.cn/ui/me")

    chosen_timeslot = input('\033[1mPlease enter your desired time slot(format: "7,8,9,10...18,19,20,21"):\033[0m')
    # timeslot format test
    while True:
        # Check if input is all digits
        if chosen_timeslot.isdigit():
            # Convert to integer
            chosen_timeslot_int = int(chosen_timeslot)
            # Check if the integer is in the timeslots keys
            if chosen_timeslot_int in timeslots:
                break  # Exit the loop if valid timeslot
            else:
                print(Fore.RED + "The timeslot is not available." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Input is not a valid number." + Style.RESET_ALL)

        # Prompt again if not valid or not available
        chosen_timeslot = input(
            'Please enter your desired time slot \033[1min format "8,9,10...19,20,21".\033[0m\n'
            'Input has to be a number from the available slots:\n')

    # Login
    while True:
        latency_part1_start = time.time()
        # Prompt the user for their account details
        account_input = input("\033[1mPlease enter your username: \033[0m")
        password_input = getpass.getpass("\033[1mPlease enter your password: \033[0m")
        captcha_input = input("\033[1mPlease enter the captcha: \033[0m")

        # Fill in the login form
        page.get_by_placeholder("Account").click()
        page.get_by_placeholder("Account").fill(account_input)
        page.get_by_placeholder("Password").click()
        page.get_by_placeholder("Password").fill(password_input)
        page.get_by_placeholder("Captcha").click()
        page.get_by_placeholder("Captcha").fill(captcha_input)
        page.get_by_role("button", name="SIGN IN").click()

        # Wait for response after login attempt
        page.wait_for_timeout(2000)  # Adjust timeout as needed

        # Check for login failure
        if page.is_visible("text=Wrong username or password") or page.is_visible("text=Wrong captcha"):
            print(Fore.RED + "Login failed. Please try again." + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "Login successful, proceeding..." + Style.RESET_ALL)
            break

    page.get_by_text("Service", exact=True).click()
    page.locator("div").filter(has_text=re.compile(r"^Sport$")).nth(1).click()
    with page.expect_popup() as page1_info:
        page.get_by_text("Sports Venue Booking 标签：暂无评分收藏").click()
    page1 = page1_info.value
    page1.get_by_placeholder("请输入场馆名称或活动类型名称").click()
    page1.get_by_placeholder("请输入场馆名称或活动类型名称").fill("羽毛球")
    page1.get_by_placeholder("请输入场馆名称或活动类型名称").press("Enter")
    time.sleep(1)

    page1.locator("li").filter(has_text="徐汇校区体育馆 地址：徐汇校区 时间：09:00-22:").get_by_role(
        "img").click()  # Xuhui

    time.sleep(1)
    page1.locator("#loginSelection").get_by_role("button", name="校内人员登录").click()
    time.sleep(1)
    page1.get_by_placeholder("请输入场馆名称或活动类型名称").click()
    time.sleep(1)
    page1.get_by_placeholder("请输入场馆名称或活动类型名称").fill("羽毛球")
    time.sleep(1)
    page1.get_by_placeholder("请输入场馆名称或活动类型名称").press("Enter")
    time.sleep(1)
    page1.locator("li").filter(has_text="徐汇校区体育馆 地址：徐汇校区 时间：09:00-22:").get_by_role(
        "img").click()  # Xuhui
    time.sleep(1)
    page1.get_by_role("tab", name="羽毛球").click()

    latency_part1_end = time.time()
    latency_part1_report = latency_part1_end - latency_part1_start
    print(f"Preparatory stage latency: {latency_part1_report:.2f} ms")
    #            ############################### PREPARE TIMES ###############################

    current_date = datetime.now(beijing)
    next_week_date = current_date + timedelta(days=7)
    date_number = next_week_date.day
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday = weekdays[next_week_date.weekday()]

    # WAITING APPROACH 1

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
                # Start countdown at 11:59:50
                for remaining in range(10, 0, -1):
                    print(f"\033[1mCountdown: {remaining} seconds left until 12:00:00\033[0m")
                    time.sleep(1)
                break
        else:
            # Refresh every minute before 11:00
            request_time_formatted = now.strftime("%H:%M:%S")
            print(f"{request_time_formatted} Waiting for the right time, refreshing every minute...")
            time.sleep(60)

    #         ############################### HERE COMES THE MAGIC ###############################
    #       ############################### WORKS, DO NOT TOUCH THIS ###############################
    # ### TEST VISIBLE + SELECTOR AT THE SAME TIME### START
    # ... [Previous countdown code]

    # After reaching the target time
    latency_part2_start = time.time()  # As fast as possible from here
    element_clicked = False
    while not element_clicked:
        page1.reload()
        try:
            # Wait for the element using wait_for_selector
            page1.get_by_role("tab", name="羽毛球").click() # maybe try without next time
            page1.wait_for_selector(f"text=月{date_number:02d}日 ({weekday})", timeout=chosen_timeout)
            page1.get_by_role("tab", name=f"月{date_number:02d}日 ({weekday})").click()
            print("\nSuccessfully accessed the booking page!")
            element_clicked = True
        except TimeoutError:
            # If wait_for_selector fails, check visibility
            if page1.is_visible(f"text=月{date_number:02d}日 ({weekday})"):
                page1.get_by_role("tab", name="羽毛球").click() # maybe try without next time
                page1.get_by_role("tab", name=f"月{date_number:02d}日 ({weekday})").click()
                print("\nSuccessfully clicked the booking tab!")
                element_clicked = True

        if element_clicked:
            latency_part2_mid = time.time()
            latency_part2_report_mid = latency_part2_mid - latency_part2_start
            print(Fore.GREEN +
                  f"Booking page accessed at {datetime.now(beijing)} in {latency_part2_report_mid:.2f} ms"
                  + Style.RESET_ALL)

        if not element_clicked:
            print(
                Fore.RED + f"Looking for 月{date_number:02d}日 ({weekday}) Element not found yet, retrying..."
                + Style.RESET_ALL)
            time.sleep(0.5)  # Brief pause before retrying

    # Proceed with the rest of the script after successfully clicking the element

    # ### TEST VISIBLE + SELECTOR AT THE SAME TIME### END
    #          ############################### HERE COMES THE MAGIC ###############################
    #       ############################### WORKS, DO NOT TOUCH THIS ###############################

    # Timeslot selection
    if chosen_timeslot == '7':
        page1.locator("div:nth-child(4) > .inner-seat > div > img").first.click()
    else:
        page1.get_by_role("tab", name="羽毛球").click() # maybe try without next time
        page1.locator(timeslots[int(chosen_timeslot)]).click()

    page1.get_by_role("button", name="立即下单").click()
    page1.locator("label span").nth(1).click()
    page1.get_by_role("button", name="提交订单").click()  # As fast as possible until here

    # Here add alternative booking dates if error

    latency_part2_end = time.time()
    latency_part2_report_end = latency_part2_end - latency_part2_start
    print(
        Fore.GREEN + f"\n\033[1mBooking completed at {datetime.now(beijing)} in {latency_part2_report_end:.2f} ms!\033[0m" + Style.RESET_ALL)
    page1.get_by_role("button", name="立即支付").click()
    page1.get_by_role("button", name="确 定").click()
    page1.get_by_role("button", name="yes").click(timeout=900000)  # Increased timeout

    # Function to wait for Enter press
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

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
