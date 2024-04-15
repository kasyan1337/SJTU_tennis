# SJTU Xuhui Campus Tennis and Badminton Court Booking Script

This script automates the booking process for tennis and badminton courts at the Shanghai Jiao Tong University (SJTU) Xuhui campus. It navigates to the booking page, waits until the booking opens at 12:00 Beijing time, and proceeds to book a slot for exactly one week ahead.

## Setup Instructions

### Prerequisites
Ensure the following prerequisites are met before running the script:
- Python is installed and added to the system PATH.
- The VPN is turned off if required to access the booking site.
- Your SJTU Jaccount language is set to English for accurate script navigation.

### Installing Dependencies
Install all necessary dependencies using the `requirements.txt` file by executing:
```bash
pip install -r requirements.txt
```
Alternatively, install the dependencies manually:
```bash
pip install pytesseract requests Pillow colorama playwright pytz
playwright install chromium
```

### Installing Animations (Optional)
For optional animations, run the following commands based on your operating system. This step is optional and only for users who want visual feedback during script execution.

For Linux:
```bash
sudo apt-get update
sudo apt-get install cmatrix
sudo apt-get install asciiquarium
```

For macOS, use Homebrew or a similar package manager:
```bash
brew install cmatrix
brew install asciiquarium
```

## Configuration (config.ini)
Before running the script, configure the `config.ini` file to match your preferences. Here are the possible parameters and their explanations:

- `booking_crontab`: Set to `ON` to enable automatic launch via crontab, `OFF` to disable it.
- `auto_launch_from_config`: Set `1` for automatic start of the script, `0` for manual start.
- `tennis_or_badminton`: Choose `t` for tennis or `b` for badminton.
- `badminton_court`: Select the court number (`1` to `4`).
- `timeslot`: Choose a time slot from `7` to `21`.
- `animations`: Set `y` to enable animations, `n` to disable them.
- `username` and `password`: Enter your SJTU Jaccount credentials.

Example section in `config.ini`:
```ini
[credentials]
booking_crontab = ON
auto_launch_from_config = 1
tennis_or_badminton = t
badminton_court = 3
timeslot = 18
username = your_username
password = your_password
animations = y
```

## Running the Script

### Manually
To run the script manually, navigate to the script's directory and run:
```bash
python SJTU_booking.py
```

### Automatically
To set up automatic execution at a specific time, use crontab on Linux or Task Scheduler on Windows. For example, to run the script daily at 11:50 AM:
```bash
crontab -e
50 11 * * * /path/to/python /path/to/SJTU_booking.py
```

## Troubleshooting
If you encounter any issues or need further assistance, contact WeChat: `kasyan98`, or submit an issue on GitHub.
