#!/usr/bin/env python3
"""Run regular checking connectivity as a background propcess separated 
   from the main program. This process will run by itself and finishes when 
   all URLs in the database can be connected successfully.There is a scheduler
   for cleaning up database which will delete all URLs in db every 5 days, thus will
   automatically stop the process."""
   
import sched, time
from datetime import datetime
import os
import sqlite3
import threading
import concurrent.futures
import requests


def check_url_status(url):
    url = url 
    r = requests.get(url)
    status_code = r.status_code
    return status_code


def notify(title, message):
    """Push Desktop notifiacation"""
    os.system("""
                osascript -e 'display notification "{}" with title "{}"'
                """.format(message, title))


def regular_check_connection(max_url_num):
    # Only check a number of top URLs in db to avoid consuming too many resources
    max_url_num = max_url_num
    db = sqlite3.connect('/Users/anhha/Documents/Projects/python-projects/urls.db')
    c = db.cursor() 
    c.execute('SELECT * FROM URLS limit ' + str(max_url_num))
    urls = c.fetchall()
    while len(urls) > 0 :
        for url in range(len(urls)):
            url_link = urls[url][0]
            db_status = urls[url][1]
            url_interval = int(urls[url][2])
            with concurrent.futures.ThreadPoolExecutor() as executor:
                current_status_check = executor.submit(check_url_status, url_link)
                current_status = current_status_check.result()
            while True:
                if int(db_status) != current_status and current_status == 200:
                    # Send nottification
                    msg = "The URL " + str(url_link) + " can be connected now!"
                    notify("Site Connectivity Check", msg)
                    print("This URL will be deleted from the current checking database.")
                    # Delete from DB
                    del_url = (url_link,)
                    c.execute('DELETE FROM URLS  WHERE Urls =?', del_url)
                    db.commit()
                    break
                else:
                    print("The URL still cannot be connected.")
                    print("Checking  " + str(url_link) + " in " + str(url_interval) + " second(s).")
                    time.sleep(url_interval)


def schedule_clean_up():
    global start_time
    endtime = datetime.now()
    # Clear db every 5 days
    if endtime.day - 5 > start_time.day:
         clear_db() 


def clear_db():
    db = sqlite3.connect('~/site-connectivity-checker/urls.db')
    msg = "Regular cleaning up database after 5 days.\
          All unconnected URLs in current checking process will be deleted."
    notify("Site Connectivity Check", msg)
    c = db.cursor() 
    c.execute('DELETE * FROM URLS')
    db.commit()
    db.close()


def main():
    start_time = datetime.now()
    regular_check_connection(10)
    schedule_clean_up()
    # Put the process in the background 
    cmd = "nohup python regular_checking.py >> /dev/null 2>&1 &"
    os.popen(cmd)
    

if __name__ == '__main__':
    main()