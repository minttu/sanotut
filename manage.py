#!venv/bin/python
# coding: utf-8

import sys
sys.dont_write_bytecode = True
import os
import config
import mysql.connector
db = mysql.connector.connect(password=config.password,
                             user=config.user,
                             host=config.host,
                             database=config.database,
                             buffered=True)

c = db.cursor()


def main():
    if "initdb" in sys.argv:
        initdb()
    elif "count" in sys.argv:
        count()


def count():
    c.execute("SELECT * FROM sanotut")
    a1 = c.fetchall()
    c.execute("SELECT * FROM sanotut_votes")
    a2 = c.fetchall()

    a1s = 0
    a2s = 0

    for a in a1:
        a1s += a[4]
    for a in a2:
        a2s += a[4]

    print "points: %i\nvotes: %i" % (a1s, a2s,)


def initdb():
    c.execute("""   CREATE TABLE IF NOT EXISTS sanotut (
                    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    time DATETIME,
                    message TEXT,
                    computer TEXT,
                    points INTEGER NOT NULL DEFAULT 0
                    );""")
    c.execute("""   CREATE TABLE IF NOT EXISTS sanotut_users (
                    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role INTEGER NOT NULL DEFAULT 0,
                    session VARCHAR(255),
                    UNIQUE (email)
                    );""")
    c.execute("""   CREATE TABLE IF NOT EXISTS sanotut_votes (
                    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    time DATETIME,
                    user_id INTEGER,
                    post_id INTEGER,
                    diff INTEGER
                    );""")

    db.commit()

if __name__ == "__main__":
    main()
