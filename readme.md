

# SJTU Xuhui Campus Tennis Court Booking Script

This script automates the booking process for tennis courts at the Shanghai Jiao Tong University (SJTU) Xuhui campus. 
It navigates to the booking page, waits until the booking opens at 12:00 Beijing time, and proceeds to book a slot for exactly one week ahead.

## Setup

Before running the script, please ensure:
- Python is installed on your system.
- All dependencies are installed. Dependencies can be found in the `requirements.txt` file. 
- Your system's VPN is turned off if required to access the booking site.
- Your SJTU Jaccount is set to English to ensure the script navigates correctly.



In case dependencies are not installed yet, execute the following command in your terminal or command prompt:
pip install -r requirements.txt

For animations, install the following:
sudo apt-get update
sudo apt-get install cmatrix

In case python is not installed yet, execute the following commands in your terminal or command prompt:

MacOS: 

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/your-username/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

brew install python


Widows: 

Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

choco install python


Regardless of your operating system, you can verify that Python is installed correctly by opening a terminal or command prompt and typing:

python --version

python3 --version


## Running the Script

To run the script, execute the following command in your terminal or command prompt:

python sjtu_tennis.py


Follow the on-screen prompts for captcha input and time slot selection.


If you encounter an error message or need further assistance, please contact me on WeChat: `kasyan98`
