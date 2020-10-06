#!/usr/bin/env python3
"""Create a site connectivity checker to check whether a webpage is live or not"""

import os, sys
import time
import re
import requests
import psutil


def check_valid_url(url):
    url = url 
    regex = re.compile(
                        r'^https?://'
                        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
                        r'localhost|'
                        r'\d{1,3}\.\d{1,3}\.\d{1,3})' 
                        r'(?::\d+)?'
                        r'(?:/?|[/?]\S+)$', re.IGNORECASE) 
    return re.match(regex, url)


def notify(title, message):
    """Push Desktop notifiacation"""
    os.system("""
                osascript -e 'display notification "{}" with title "{}"'
                """.format(message, title))


def start_process(url):
    url = url 
    r = requests.get(url)
    if r.status_code not in range(399, 600):
        msg = "Successful Connection! Status code is " + str(r.status_code)  
    else:
        msg = "Bad status code: "  + str(r.status_code) 
    return msg 


def stop_process(*args):
    if len(args) != 0:
        url = args
        cmd = "ps -ef | grep 'site-connectivity-check " + str(url) + "' | tail -1 | awk '{print $2}'"
    else:
        #If the user not specify URL, terminate the current one
        cmd = "ps -ef | grep 'site-connectivity-check' | tail -1 | awk '{print $2}'"
    pid = int(os.popen(cmd).read().strip("\n"))
    print(pid)
    process_id = psutil.Process(pid)
    print("Stop check-connect program.")
    process_id.terminate()


def regular_check(url, interval):
    url = url 
    interval = int(interval)
    r = requests.get(url)
    while True: 
        if r.status_code not in range(399, 600):
            msg = "The URL " + str(url) + " can be connected now!"
            notify("Site Connectivity Check", msg)   
        else:
            msg = "Still cannot connect to " + str(url) + ". Continue checking process."
            time.sleep(interval)  

