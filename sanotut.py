#!venv/bin/python
# coding: utf-8

import sys
sys.dont_write_bytecode = True
import os
import re
import pwd
import string
import random

import config

from passlib.apps import custom_app_context as pwd_context

from flask import Flask, render_template, flash, redirect, request, abort, session
app = Flask(__name__, template_folder="sanotut/templates",
            static_folder="sanotut/static")
app.config["SECRET_KEY"] = config.secret

import mysql.connector
db = mysql.connector.connect(password=config.password,
                             user=config.user,
                             host=config.host,
                             database=config.database,
                             buffered=True)

c = db.cursor()

import datetime


def checksesval():
    if "sesval" not in session:
        return None
    if "email" not in session:
        return None
    if "logged_in" not in session:
        return None
    c.execute(
        "SELECT * FROM sanotut_users WHERE session = (%s) AND email = (%s)", (session["sesval"], session["email"],))
    res = c.fetchone()
    if res == None:
        return None
    if len(res[4]) == 64:
        return res[0]
    return None


def validemail(email):
    if email == None:
        return False
    m = re.match("^(\w+)@paivola.fi$", email)
    if m == None:
        return False
    if config.realaccouts:
        try:
            pwd.getpwnam(m.group(1))
        except KeyError:
            return False
    return True


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


@app.route('/register')
def route_register():
    return render_template("register.html")


@app.route('/onregister', methods=['POST'])
def route_onregister():
    if "email" not in request.form or not validemail(request.form["email"]):
        flash(u"Sähköposti ei vastaa vaadittua kaavaa!")
        return redirect("/register")
    if "password" not in request.form or len(request.form["password"]) < 6:
        flash(u"Salasanasi tulee olla yli viisi merkkiä!")
        return redirect("/register")
    hash = pwd_context.encrypt(request.form["password"])

    try:
        c.execute("""INSERT INTO sanotut_users
                     (email, password)
                     VALUES (%s, %s)""",
                 (request.form["email"], hash,))
    except Exception:
        flash(u"Tuo sposti on rekisteröity jo!")
        return redirect("/register")

    db.commit()

    flash(u"Voit nyt kirjautua sisään!")
    return redirect("/login")


@app.route('/login')
def route_login():
    return render_template("login.html")


@app.route('/onlogin', methods=['POST'])
def route_onlogin():
    if "email" not in request.form or "password" not in request.form:
        flash(u"Anna sposti ja salasana.")
        return redirect("/login")
    c.execute("""   SELECT * FROM sanotut_users
                    WHERE email = (%s)""", (request.form["email"],))
    res = c.fetchone()
    if res == None or not pwd_context.verify(request.form["password"], res[2]):
        flash(u"Ei moista sposti/salasana paria!")
        return redirect("/login")
    allchoice = string.lowercase + string.uppercase + string.digits
    sesval = ''.join(random.choice(allchoice) for i in range(64))

    c.execute("UPDATE sanotut_users SET session = (%s) WHERE id = (%s)",
             (sesval, res[0],))
    db.commit()

    session["sesval"] = sesval
    session["email"] = request.form["email"]
    session["logged_in"] = True

    flash(u"Kirjauduit sisään.")
    return redirect("/")


@app.route('/logout')
def route_logout():
    uid = checksesval()
    if uid == None:
        flash(u"Olet jo kirjautunut ulos.")
        return render_template("/")
    c.execute("UPDATE sanotut_users SET session = NULL WHERE id = (%s)",
             (uid,))
    del session["sesval"]
    del session["email"]
    del session["logged_in"]
    flash(u"Olet kirjautunut ulos.")
    return redirect("/")


@app.route('/onvote', methods=['POST'])
def route_vote():
    if request.data == None:
        abort(400)

    uid = checksesval()
    if uid == None:
        return u"error: et ole kirjautunut sisään", 400

    spl = request.data.split(":")
    if len(spl) != 2:
        abort(400)
    meth = spl[0]
    id = int(spl[1])
    amount = 0
    if meth == "up":
        amount = 1
    elif meth == "down":
        amount = -1
    else:
        return "error: unkown method", 400

    c.execute(
        "SELECT * FROM sanotut_votes WHERE post_id=(%s) AND user_id=(%s)", (id, uid,))
    earlier = c.fetchone()
    if earlier != None:
        #if earlier[4] == amount:
        return u"error: olet jo äänestänyt tuota", 400
        #else:
        #    c.execute(
        #        "UPDATE sanotut_votes SET diff=(%s) WHERE id=(%s)", (amount, earlier[0],))
    else:
        c.execute(
            "INSERT INTO sanotut_votes (time, user_id, post_id, diff) VALUES (%s, %s, %s, %s)",
            (datetime.datetime.now(), uid, id, amount))

    c.execute(
        "UPDATE sanotut SET points=points+(%(amount)s) WHERE id=(%(id)s)",
        {"amount": amount, "id": id})
    db.commit()
    return "success:%s:%i" % (meth, id), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
