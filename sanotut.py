#!../../venv/bin/python
# coding: utf-8

from flask import Flask, render_template, flash, redirect, request, abort
app = Flask(__name__, template_folder="sanotut/templates")

import sys
sys.dont_write_bytecode = True
import os
import config
import mysql.connector
db = mysql.connector.connect(password = config.password,
                             user = config.user,
                             host = config.host,
                             database = config.database,
                             buffered = True)

c = db.cursor()

import datetime

@app.route('/')
def route_index():
    c.execute(("SELECT * FROM sanotut ORDER BY id DESC"))
    entries = c.fetchall()
    return render_template("index.html", entries=entries)

@app.route('/add')
def route_add():
    return render_template("add.html")

@app.route('/onadd', methods=['POST'])
def route_onadd():
    if "sanottu" not in request.form:
        abort(400)
    c.execute(("INSERT INTO sanotut"
               "(message, computer, time)"
               "VALUES (%(message)s, %(computer)s, %(time)s)"),
               {"message": request.form["sanottu"].replace("<", "&lt;").replace(">", "&gt;"),
                "computer": request.remote_addr,
                "time": datetime.datetime.now()})
    db.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
