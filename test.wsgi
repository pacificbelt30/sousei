[uwsgi]
plugin = python3
module = app
callable = app
master = true
processes = 1
socket = /tmp/uwsgi.sock
chmod-socket = 666
vacuum = true
die-on-term = true
wsgi-file = /home/user/work/sousei/run.py
logto = /var/log/uwsgi.log
