sanotut
==========

Database for quotes. Beta quality.

TODO
====

* Support more than 1 session per user at a time
* Alternative style
* Clean code

install
=======

    virtualenv venv
    ./venv/bin/pip install -r requirements.txt
    setup some rerouting
    ./manage initdb

    for developing: ./sanotut.py
    for deployment: there is sanotut/index.cgi
