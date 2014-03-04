sanotut.py
==========

Database for quotes. Beta quality. Flat theme is not ready for production!

TODO
====

* Support more than 1 session per user at a time
* Alternative style
* Clean code

install
=======

    create a config.py with user, host, database, password, secret, (boolean) realaccouts
    virtualenv venv
    ./venv/bin/pip install -r requirements.txt
    setup some rerouting
    ./manage initdb

    for developing: ./sanotut.py
    for deployment: there is sanotut/index.cgi
