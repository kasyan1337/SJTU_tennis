

# SJTU Xuhui Campus Tennis Court Booking Script

This script automates the booking process for tennis courts at the Shanghai Jiao Tong University (SJTU) Xuhui campus. 
It navigates to the booking page, waits until the booking opens at 12:00 Beijing time, and proceeds to book a slot for exactly one week ahead.

## Setup

Before running the script, please ensure:
- Python is installed on your system.
- All dependencies are installed. Dependencies can be found in the `requirements.txt` file. 
- Your system's VPN is turned off if required to access the booking site.
- Your SJTU Jaccount is set to English to ensure the script navigates correctly.

- In case dependencies are not installed yet, execute the following command in your terminal or command prompt:
pip install -r requirements.txt
or manually:
pip install pytesseract requests Pillow colorama playwright pytz
playwright install chromium

- For animations, install the following:
sudo apt-get update
sudo apt-get install cmatrix
sudo apt-get install asciiquarium

## Running the Script

To run the script, execute the following command in your terminal or command prompt:

python SJTU_booking.py

If you encounter an error message or need further assistance, please contact me on WeChat: `kasyan98`
