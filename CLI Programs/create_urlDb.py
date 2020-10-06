#!/usr/bin/env python3
"""This program create URL database for background checking process."""

import sqlite3


def create_db_tbl():
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    # Create URLS Table
    c.execute('''CREATE TABLE URLS
                (Urls text, Status , Interval integer)''')
    #Insert a row of data to test
    c.execute("INSERT INTO URLS VALUES ('https://github.com', '400', '60')")
    # Save the changes
    conn.commit()
    conn.close()


def test_db():
    conn = sqlite3.connect('~/site-connectivity-checker/urls.db/urls.db')
    c = conn.cursor()
    url = ('https://github.com',)
    c.execute('SELECT * FROM URLS WHERE Urls =?', url)
    status = c.fetchall()
    print(status)


def drop_table():
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('DROP TABLE URLS')


def main():
    create_db_tbl()
    # test_db()
    # drop_table()


if __name__ == '__main__':
    main()