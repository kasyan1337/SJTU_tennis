import re
import time
from datetime import datetime, timedelta

from playwright.sync_api import Playwright, sync_playwright
from playwright.sync_api import TimeoutError
from pytz import timezone

timeslots_1court = {
    8: "div:nth-child(3) > .seat > .inner-seat > div",
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

court_number = None
timeslots_8courts = {
    8: f"div:nth-child(3) > div:nth-child({court_number}) > .inner-seat > div",
    9: f"div:nth-child(4) > div:nth-child({court_number}) > .inner-seat > div",
    10: f"div:nth-child(5) > div:nth-child({court_number}) > .inner-seat > div",
    11: f"div:nth-child(6) > div:nth-child({court_number}) > .inner-seat > div",
    12: f"div:nth-child(7) > div:nth-child({court_number}) > .inner-seat > div",
    13: f"div:nth-child(8) > div:nth-child({court_number}) > .inner-seat > div",
    14: f"div:nth-child(9) > div:nth-child({court_number}) > .inner-seat > div",
    15: f"div:nth-child(10) > div:nth-child({court_number}) > .inner-seat > div",
    16: f"div:nth-child(11) > div:nth-child({court_number}) > .inner-seat > div",
    17: f"div:nth-child(12) > div:nth-child({court_number}) > .inner-seat > div",
    18: f"div:nth-child(13) > div:nth-child({court_number}) > .inner-seat > div",
    19: f"div:nth-child(14) > div:nth-child({court_number}) > .inner-seat > div",
    20: f"div:nth-child(15) > div:nth-child({court_number}) > .inner-seat > div",
    21: f"div:nth-child(16) > div:nth-child({court_number}) > .inner-seat > div"}

beijing = timezone('Asia/Shanghai')


def check_if_past_12_15():
    """
    This function checks if it is past 12:15 PM.
    If it is, it prints a message and quits the script.
    :return:
    """
    current_datetime = datetime.now(beijing)
    cutoff_time = current_datetime.replace(hour=12, minute=15, second=0, microsecond=0)
    # Check if the current time is past the cutoff time
    if current_datetime > cutoff_time:
        print("It is past 12:15 PM. You should try again tomorrow.")
        quit()
    else:
        # Calculate the date 7 days from now
        future_date = current_datetime + timedelta(days=7)

        # Format the date as "Weekday, Month day, Year"
        future_date_formatted = future_date.strftime("%A, %B %d, %Y")

        # Use the formatted date in the print statement
        print(f"You are booking the tennis court for {future_date_formatted}")


def login():
    """
    This function logs you in to the booking page.
    :return: username + pw
    """
    print(
        "This is a script that books a tennis court on SJTU Xuhui campus.\n"
        "Script navigates you to the booking page, then waits for 12:00:01(Beijing time) for the booking to open,"
        " then proceedes.\n"
        "Script supports booking only one week ahead, meaning if today is Monday 11:00AM, "
        "you're booking for next Monday.\n"
        "Otherwise ur lazy ass can just do it yourself without the script. \n"
        "Script is going to need 4 user inputs, if u accidentally make a mistake in any of them, "
        "close the whole thing and rerun the script.\n"
        "If you get an error message, send it together with hongbao to: Wechat ID: kasyan98\n"
        "Enjoy xoxo")

    account_input = input("Please enter your account: ")
    password_input = input("Please enter your password: ")
    captcha_input = input("Please enter the captcha: ")

    return account_input, password_input, captcha_input


def login_check():
    """
    Check if login successful, if not print why and call login again
    :return: #TODO implement
    """
    # These two elements cannot be on page
    page.get_by_text("Wrong username or password").click()
    page.get_by_text("Wrong captcha").click()
    pass


def choose_location():
    """
    This function chooses the location of the court.
    :return:
    """
    where_book_input = input('Choose location\n'
                             'Type "1" for "子衿街南侧网球场"\n'
                             'Type "2" for "东区网球场"\n'
                             'Type "3" for "胡晓明网球场"\n'
                             'Type "4" for "徐汇校区网球场"\n')

    # Test if where_book_input correct format
    while True:
        if where_book_input not in ["1", "2", "3", "4"]:
            print("Invalid input")
            where_book_input = input('Choose location\n'
                                     'Type "1" for "子衿街南侧网球场"\n'
                                     'Type "2" for "东区网球场"\n'
                                     'Type "3" for "胡晓明网球场"\n'
                                     'Type "4" for "徐汇校区网球场"\n')
        elif where_book_input == "1" or "4":
            timeslots = timeslots_1court
            return timeslots
        elif where_book_input == "2" or "3":
            timeslots = timeslots_8courts
            return timeslots


def choose_court():
    """
    This function chooses the court number.
    :return:
    """
    if where_book_input == "2" or "3":
        court_number_input = input("Choose court number(1-8)")

        while True:
            if int(court_number_input) < 1 or int(court_number_input) > 8:
                print("Invalid input")
                court_number_input = input("Choose court number(1-8)")
            else:
                court_number_input = court_number
                break


def choose_timeslot():
    """
    This function chooses the timeslot.
    :return:
    """
    chosen_timeslot = input('Please enter your desired time slot(format: "7,8,9,10...18,19,20,21"):')
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
                print("The timeslot is not available.")
        else:
            print("Input is not a valid number.")

        # Prompt again if not valid or not available
        chosen_timeslot = input(
            'Please enter your desired time slot in format "8,9,10...19,20,21".\n'
            'Input has to be a number from the available slots:\n')


def wait_until_12():
    """
    This function waits until 12:00:00.
    :return:
    """
    current_date = datetime.now(beijing)
    next_week_date = current_date + timedelta(days=7)
    date_number = next_week_date.day
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday = weekdays[next_week_date.weekday()]

    # WAITING APPROACH 1

    # Adjusted loop for waiting until 12:00:00, with countdown
    while True:
        now = datetime.now(beijing)
        if now.hour == 11 and now.minute >= 59 and now.second >= 50:
            # Start countdown from 11:59:50
            for remaining in range(10 - (now.second - 50), 0, -1):
                print(f"Countdown: {remaining} seconds left until 12:00:00")
                time.sleep(1)
            break
        else:
            request_time_formatted = now.strftime("%H:%M:%S")
            print(f"{request_time_formatted} Waiting for magic to happen, refreshing...")
            time.sleep(10)


def book():
    """
    This function books the court.
    :return:
    """
    current_date = datetime.now(beijing)
    next_week_date = current_date + timedelta(days=7)
    date_number = next_week_date.day
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday = weekdays[next_week_date.weekday()]

    latency_part2_start = time.time()
    element_clicked = False
    while not element_clicked:
        page1.reload()  # TODO nejako to spojit, nech to berie referenciu na page1
        try:
            # Wait for the element to be present before clicking, with a timeout
            page1.wait_for_selector(f"role=tab[name='月{date_number:02d}日 ({weekday})']", timeout=1000)
            page1.get_by_role("tab", name=f"月{date_number:02d}日 ({weekday})").click()
            latency_part2_mid = time.time()
            latency_part2_report_mid = latency_part2_mid - latency_part2_start
            print(f"Successfully clicked the booking tab.\n"
                  f"Booking page accessed in {latency_part2_report_mid:.2f} ms")
            element_clicked = True
        except TimeoutError:
            print("Element not found yet, retrying...")
            # If the element isn't found within the timeout period, it retries
        except Exception as e:
            print(f"Encountered an error: {e}, retrying after a brief pause...")
            time.sleep(0.5)  # Brief pause before retrying, to handle load issues or other errors

    # Proceed with the rest of the script after successfully clicking the element

    # Timeslot selection
    if chosen_timeslot == '7':
        page1.locator(".inner-seat > div").first.click()
    else:
        page1.locator(timeslots[int(chosen_timeslot)]).click()

    page1.get_by_role("button", name="立即下单").click()
    page1.locator("label span").nth(1).click()
    page1.get_by_role("button", name="提交订单").click()
    latency_part2_end = time.time()
    latency_part2_report_end = latency_part2_end - latency_part2_start
    print(f"Booking completed in {latency_part2_report_end:.2f} ms")
    page1.get_by_role("button", name="立即支付").click()
    page1.get_by_role("button", name="确 定").click()
    page1.get_by_role("button", name="yes").click()


def pay():
    """
    This function pays for the court.
    :return:
    """
    pass


def run(playwright: Playwright) -> None:
    """
    This is a script that books a tennis court in SJTU Xuhui campus.
    Script navigates you to the booking page, then waits for 12:00:01(Beijing time), for the booking to open, then proceedes.
    Script supports booking only one week ahead, meaning if today is Monday 11:00AM, you're booking for next Monday.
    Otherwise ur lazy ass can just do it on ur own without the script.
    Script is going to need x user inputs, if u accidentally make a mistake in any of them, close the whole thing and rerun the script.
    If you get an error message, send it together with hongbao to: Wechat ID: kasyan98
    Enjoy xoxo
    """

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(
        "https://my.sjtu.edu.cn/ui/me")

    login()
    choose_location()
    choose_court()
    choose_timeslot()

    latency_part1_start = time.time()

    page.get_by_placeholder("Account").click()
    page.get_by_placeholder("Account").fill(account_input)
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill(password_input)
    page.get_by_placeholder("Captcha").click()
    page.get_by_placeholder("Captcha").fill(captcha_input)
    page.get_by_role("button", name="SIGN IN").click()
    page.get_by_text("Service", exact=True).click()
    page.locator("div").filter(has_text=re.compile(r"^Sport$")).nth(1).click()
    with page.expect_popup() as page1_info:
        page.get_by_text("Sports Venue Booking 标签：暂无评分收藏").click()
    page1 = page1_info.value
    page1.get_by_placeholder("请输入场馆名称或活动类型名称").click()
    page1.get_by_placeholder("请输入场馆名称或活动类型名称").fill("网球")
    page1.get_by_placeholder("请输入场馆名称或活动类型名称").press("Enter")

    # page1.locator("li").filter(has_text="胡晓明网球场 地址：闵行校区 时间：07:00-22:").get_by_role("img").click() # Minhang
    page1.locator("li").filter(has_text="徐汇校区网球场 地址：徐汇校区 时间：07:00-22:").get_by_role(
        "img").click()  # Xuhui

    page1.locator("#loginSelection").get_by_role("button", name="校内人员登录").click()
    page1.get_by_placeholder("请输入场馆名称或活动类型名称").click()
    page1.get_by_placeholder("请输入场馆名称或活动类型名称").fill("网球")
    page1.get_by_placeholder("请输入场馆名称或活动类型名称").press("Enter")
    # page1.locator("li").filter(has_text="胡晓明网球场 地址：闵行校区 时间：07:00-22:").get_by_role("img").click() # Minhang
    page1.locator("li").filter(has_text="徐汇校区网球场 地址：徐汇校区 时间：07:00-22:").get_by_role(
        "img").click()  # Xuhui

    latency_part1_end = time.time()
    latency_part1_report = latency_part1_end - latency_part1_start
    print(f"Preparatory stage latency: {latency_part1_report:.2f} ms")
    # ############################### HERE COMES THE MAGIC ###############################

    wait_until_12()
    book()

    # ############################### HERE COMES THE MAGIC ###############################

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
