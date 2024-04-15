import configparser
import os


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


    username_zsh = os.getenv('SJTU_USERNAME')
    user_password_zsh = os.getenv('SJTU_USER_PASSWORD')

    return username_config, user_password_config, timeslot_config, badminton_court_config, animations_config, tennis_or_badminton_config


username = config_parser()[0]
user_password = config_parser()[1]
timeslot = config_parser()[2]
badminton_court = config_parser()[3]
animations = config_parser()[4]
tennis_or_badminton_config = config_parser()[5]

print(username, user_password, timeslot, badminton_court, animations, tennis_or_badminton_config)


