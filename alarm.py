# alarm clock utility to be used with shell
# Yan Kostadinov 02/08/2018

import re
import random
import webbrowser
import datetime
import time
from threading import Timer

# Default list of youtube videos to be included
DEFAULT_URLS = ['https://youtu.be/TEDiegpFsQM',
                'https://youtu.be/YthChN1Wq8M',
                'https://youtu.be/HBB37gsHJmQ',
                'https://youtu.be/CSvFpBOe8eY',
                'https://youtu.be/IcrbM1l_BoI']

# Regex to check if the URL read is a valid youtube URL
URL_REGEX = re.compile(r"^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$")
# Regex to check if the time enter is in valid format
TIME_REGEX = re.compile(r"^\s*([0-2]?\d):?([1-5]\d)?\s*(am|pm)?s*", re.IGNORECASE)

def open_urls(filename="videos.txt"):
    '''Tries opening a file with name "filename" (default "videos.txt") in the current working directory - if file doesn't exist, creates it.
    Then extracts all the valid YouTube URLs from the file and returns them in a list.'''
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            video_urls = list(url.strip() for url in f.readlines() if URL_REGEX.match(url.strip()))
        if video_urls == []:
            with open(filename, 'w') as f:
                f.writelines('\n'.join(DEFAULT_URLS))
                video_urls = list.copy(DEFAULT_URLS)
    except FileNotFoundError:
        with open(filename, 'w') as f:
            f.writelines('\n'.join(DEFAULT_URLS))
            video_urls = list.copy(DEFAULT_URLS)
    finally:
        return video_urls


def open_random_video(video_urls=DEFAULT_URLS[:]):
    '''Accepts a list, takes only the valid YouTube URLs from it and opens a random URL in a new browser tab.
    If the list doesn't contain any valid URLs, throws IOError'''
    valid_urls = list(filter(URL_REGEX.match, video_urls))
    if valid_urls == []:
        raise IOError("No valid URLs found in the file.")
    webbrowser.open_new_tab(random.choice(valid_urls))


def get_time():
    '''Accepts a user input in valid time format and returns the time left until the alarm in seconds'''
    try:
        print("When should the alarm ring? (Type \"quit\" to stop the program)")
        user_input = input()
        while not TIME_REGEX.match(user_input):
            if "quit" in user_input.lower():
                raise KeyboardInterrupt
            print("You must use one of these time formats:\n20:50\n11:34am\n3pm")
            print("\nWhen should the alarm ring? (Type \"quit\" to stop the program)")
            user_input = input()

        valid_time = TIME_REGEX.match(user_input)
        # create variables to initialize the alarm datetime object
        alarm_hours = int(valid_time.group(1))
        alarm_minutes = int(valid_time.group(2)) if valid_time.group(2) else 0
        am_pm = valid_time.group(3).upper() if valid_time.group(3) else ""

        if alarm_hours == 12:
            alarm_hours = 0 if "A" in am_pm else 12
        elif "P" in am_pm:
            alarm_hours = int(alarm_hours) + 12

        time_now = datetime.datetime.today()
        # creates a datetime object for tomorrow, thus saving us the trouble of figuring out if today is 31st of a month
        # then tomorrow is going to be the next month, but if the current month is December, then the year, etc.
        time_tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)

        if alarm_hours < time_now.hour or (alarm_hours == time_now.hour and alarm_minutes <= time_now.minute):
            alarm_year = time_tomorrow.year
            alarm_month = time_tomorrow.month
            alarm_day = time_tomorrow.day
        else:
            alarm_year = time_now.year
            alarm_month = time_now.month
            alarm_day = time_now.day

        alarm_time = datetime.datetime(year=alarm_year, month=alarm_month, day=alarm_day, hour=alarm_hours,
                                       minute=alarm_minutes)
        return (alarm_time - time_now).seconds

    except KeyboardInterrupt:
        print('\nNo alarm for you then.')
        time.sleep(1)
        exit()

def run_alarm(alarm_time=0, video_urls=DEFAULT_URLS):
   '''Uses Timer from threading to open a random video from a list of URLs in alarm_time (must be seconds)'''
   alarm_timer = Timer(alarm_time, open_random_video, args=([video_urls]))
   alarm_timer.start()
   print("Your alarm will run in %s seconds, please don't close this window or it won't run." % alarm_time)


if __name__ == "__main__":
    video_urls = open_urls()
    alarm_time = get_time()
    run_alarm(alarm_time,video_urls)
