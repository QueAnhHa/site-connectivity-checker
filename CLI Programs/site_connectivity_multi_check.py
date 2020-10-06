#!/usr/bin/env python3

"""Command line interface program to check whether a webpage is live or not.
The program can take multiples URLs and stores in database for frequently checking.
When a site is connected successfully, the bacground process regular_checking will send 
a Desktop notification to the user."""

import argparse 
import os, sys
import re
import sqlite3
from tabulate import tabulate
import requests
import psutil
import regular_checking


def get_user_input():
    # Create the top level parser: check-connect
    parser = argparse.ArgumentParser(description="Check Site Connectivity") 
    subparsers = parser.add_subparsers(help='subcommand help')

    # Create the parser for "start" command
    parser_start = subparsers.add_parser('start', help="Starting to check the url connection.")
    parser_start.add_argument('url', type=str, help="URL for connectitivy check, \
                             must be a valid URL (example: http://google.com).")
    parser_start.add_argument('-interval', '-i', type=int, default=60, help="Specify checking interval \
                             in seconds, default is 60s.")

    # Create the parser for "stop" command
    parser_stop = subparsers.add_parser('stop', help="Stopping the checking process.")
    parser_stop.add_argument('-url', '-u', nargs='?', type=str, default='*', help="Stop checking a specific URL \
                             and delete it from database.If not specified, default to all.")
    
    # Create a parser for "show" command
    parser_show = subparsers.add_parser('show', help="Showing current status of URL(s) in database.")
    parser_show.add_argument('-url', '-u', type=str, default='*', help="A specific URL for status checking \
                            in database.If not specify, default to all.")

     # Create a parser for "silent" command - run the regular checking process in background
    parser_silent = subparsers.add_parser('silent', help="Activate frequent checking process in background. \
                                         Send Desktop notification when site can be connected. Automatically \
                                         stop checking after 5 days.")

    args = parser.parse_args() 
    return args 


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


def check_url_status(url):
    url = url 
    r = requests.get(url)
    status_code = r.status_code
    return status_code


def check_connection():
    user_input = get_user_input()
    cmd = sys.argv[1]
    url = user_input.url 
    db = sqlite3.connect('~/site-connectivity-checker/urls.db')
    c = db.cursor()

    if cmd == 'start':
        interval = user_input.interval
        if check_valid_url(url):
            status = check_url_status(url)
            db_url = (url,) 
            c.execute('SELECT * FROM URLS WHERE Urls =?', db_url)
            url_exist = c.fetchall()
            if len(url_exist) != 0: 
                print("This URL is in our database for frequent connectivity check.")
                c.execute('SELECT Status FROM URLS WHERE Urls =?', db_url)
                db_status = c.fetchone()[0]
                print("Current status of this URL in database is " + str(db_status))
                print("Will send you notification when the site can be connected.")
                db.close()
            else: # No record
                if status not in range(399, 600):
                    print("Connection to " + str(url) + "successful! Please check it on your web browser.")
                else:
                    print("Get bad status code. Writing the url to checking database.")
                    print("Will recheck the site connectivity in " + 
                           str(interval) + " second(s) .")
                    print("Will send you notification when the site can be connected.") 
                    cmd = "INSERT INTO URLS VALUES ('" + str(url) + "', '" + str(status) + "', " + str(interval) + " )"
                    c.execute(cmd)
                    db.commit()
                    db.close()        
        else: 
            print("Not a valid URL.")
    elif cmd == 'stop':
        if url != '*':
            print("Stopping checking connectivity.")
            print("Deleting the URL from checking database.")
            db_url = (url,)
            c.execute('DELETE FROM URLS  WHERE Urls =?', db_url)
            db.commit()
            db.close()
        else:
            print("Deleting all URLs infromation from checking database.")
            c.execute('DELETE * FROM URLS')
            db.commit()
            db.close()
    elif cmd == 'show':
        if url != '*':
            db_url = (url,)
            c.execute('SELECT * FROM URLS WHERE Urls =?', db_url)
            status = c.fetchall()
            if len(status) > 0:
                print(tabulate(status, headers=['URL', 'Status', 'Interval Check'], tablefmt='orgtbl'))
            print("This URL is not in current checking database.")
            db.close()
        else:
            c.execute('SELECT * FROM URLS')
            status = c.fetchall()
            print(tabulate(status, headers=['URL', 'Status', 'Interval Check'], tablefmt='orgtbl'))
            db.close()
    else:
        regular_checking()


def main():
    check_connection()


if __name__ == '__main__':
    main()