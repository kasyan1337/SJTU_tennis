import re
import time
from datetime import datetime, timedelta

from playwright.sync_api import Playwright, sync_playwright
from playwright.sync_api import TimeoutError


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(
        "https://my.sjtu.edu.cn/ui/me")

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

    # account_input = input("Please enter your account: ")
    # password_input = input("Please enter your password: ")
    captcha_input = input("Please enter the captcha: ")

    # current_datetime = datetime.now(beijing)
    # cutoff_time = current_datetime.replace(hour=12, minute=30, second=0, microsecond=0)
    # # Check if the current time is past the cutoff time
    # if current_datetime > cutoff_time:
    #     print("It is past 12:30 PM. You should try again tomorrow.")
    #     quit()
    # else:
    #     # Calculate the date 7 days from now
    #     future_date = current_datetime + timedelta(days=7)
    #
    #     # Format the date as "Weekday, Month day, Year"
    #     future_date_formatted = future_date.strftime("%A, %B %d, %Y")
    #
    #     # Use the formatted date in the print statement
    #     print(f"You are booking the tennis court for {future_date_formatted}")

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

    latency_part1_start = time.time()

    page.get_by_placeholder("Account").click()
    page.get_by_placeholder("Account").fill("kasim.janci98")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("USBcable1234")
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

    # After reaching the target time
    latency_part2_start = time.time()
    element_clicked = False
    while not element_clicked:
        page1.reload()
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

    # ############################### HERE COMES THE MAGIC ###############################

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

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
