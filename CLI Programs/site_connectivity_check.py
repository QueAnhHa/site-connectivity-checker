#!/usr/bin/env python3
"""A program to check whether a webpage is live or not"""

import argparse 
import os, sys
import time
import re
try:
    import requests
except ImportError:
    print(sys.exc_info())
try:
    import psutil
except ImportError:
    print(sys.exc_info())


def get_user_input():
    # Create the top level parser: check-connect
    parser = argparse.ArgumentParser(description="Check Site Connectivity") 
    subparsers = parser.add_subparsers(help='subcommand help')

    # Create the parser for "start" command
    parser_start = subparsers.add_parser('start', help='Starting to check the url connection ')
    parser_start.add_argument('url', type=str, help="URL for connectitivy check, must be a valid \
                             URL (example: http://google.com).")
    parser_start.add_argument('-interval', type=int, default=60, help="Specify checking interval \
                            in seconds, default is 60s.")

    # Create the parser for "stop" command
    parser_stop = subparsers.add_parser('stop', help="Stopping the checking process")
    parser_start.add_argument('-url', type=str, help="URL for connectitivy check")

    args = parser.parse_args()
    return args 


def check_valid_url(url):
    url = url 
    regex = re.compile(
                        r'^https?://'
                        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|' #domain
                        r'localhost|'
                        r'\d{1,3}\.\d{1,3}\.\d{1,3})' #...or ip
                        r'(?::\d+)?' #optional port
                        r'(?:/?|[/?]\S+)$', re.IGNORECASE) 
    return re.match(regex, url)


def start_process(url, interval):
    url = url 
    interval = int(interval)
    r = requests.get(url)
    while True:
        if r.status_code not in range(399, 600):
            print("Connection to " + str(url) + "successful! Please check it on your web browser.") 
            break    
        else:
            print("We get bad status code. Keep checking the site connectivity in " + 
                  str(interval) + " second(s) .")
            time.sleep(interval) 


def stop_process(*args):
    if len(args) != 0:
        url = args
        cmd = "ps -ef | grep 'check-connect start " + str(url) + "' | tail -1 | awk '{print $2}'"
    else:
        # If the user not specify URL, terminate the current one
        cmd = "ps -ef | grep 'check-connect start' | tail -1 | awk '{print $2}'"
    pid = int(os.popen(cmd).read().strip("\n"))
    print(pid)
    process_id = psutil.Process(pid)
    print("Stop check-connect program.")
    process_id.terminate()

    
def check_connect():
    user_input = get_user_input()
    cmd = sys.argv[1]
    if cmd == 'start' and check_valid_url(user_input.url):
        url = user_input.url 
        interval = user_input.interval
        start_process(url, interval)
    elif cmd == 'stop':
        if user_input.url and check_valid_url(user_input.url):
            url = user_input.url 
            stop_process(url)
        else:
            stop_process()
    else: 
        print("Not a valid URL.")


def main():
    check_connect()


if __name__ == '__main__':
    main()