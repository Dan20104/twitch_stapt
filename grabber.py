#! /usr/bin/python3
import os
from datetime import datetime, timedelta
from urllib.parse import urlparse

import pytz
import requests
from lxml import etree
from bs4 import BeautifulSoup

tz = pytz.timezone('Europe/London')
channels = []


def generate_times(curr_dt: datetime):
    """
Generate 3-hourly blocks of times based on a current date
    :param curr_dt: The current time the script is executed
    :return: A tuple that contains a list of start dates and a list of end dates
    """
    # Floor the last hour (e.g. 13:54:00 -> 13:00:00) and add timezone information
    last_hour = curr_dt.replace(microsecond=0, second=0, minute=0)
    last_hour = tz.localize(last_hour)
    start_dates = [last_hour]

    # Generate start times that are spaced out by three hours
    for x in range(7):
        last_hour += timedelta(hours=3)
        start_dates.append(last_hour)

    # Copy everything except the first start date to a new list, then add a final end date three hours after the last
    # start date
    end_dates = start_dates[1:]
    end_dates.append(start_dates[-1] + timedelta(hours=3))

    return start_dates, end_dates


def grab_twitch(url: str):
    """

    :param url:
    :return:
    """
    requests.packages.urllib3.disable_warnings()
    stream_info = requests.get(url, timeout=15)
    soup = BeautifulSoup(stream_info.text, features="html.parser")

    if stream_info.status_code != 200:
        print("https://github.com/ExperiencersInternational/tvsetup/raw/main/staticch/no_stream_2.mp4")
        return

    response = requests.get(f"https://pwn.sh/tools/streamapi.py?url={url}").json()["success"]
    if response == "false":
        print("https://github.com/ExperiencersInternational/tvsetup/raw/main/staticch/no_stream_2.mp4")
        return
    url_list = requests.get(f"https://pwn.sh/tools/streamapi.py?url={url}").json()["urls"]
    max_res_key = list(url_list)[-1]
    stream_url = url_list.get(max_res_key)
    print(stream_url)

# Open text file and parse stream information and URL
with open('./streams.txt', encoding='utf-8') as f:
    print("#EXTM3U")
    for line in f:
        line = line.strip()
        if not line or line.startswith('##'):
            continue
        if not (line.startswith('https:') or line.startswith('http:')):
            print(
                f'\n#EXT-X-STREAM-INF:PROGRAM-ID=1, BANDWIDTH=737777')
        else:
            elif urlparse(line).netloc == 'www.twitch.tv':
                grab_twitch(line)

# Remove temp files from project dir
if 'temp.txt' in os.listdir():
    os.system('rm temp.txt')
    os.system('rm watch*')
