#cd /var/flask_app && uwsgi_python3 --ini uwsgi.ini & nginx -g "daemon off;"
cd /var/flask_app && nginx & uwsgi_python3 --ini uwsgi.ini 
#/bin/bash
#cd /var/flask_app
#python3 run.py
# GRANT SELECT,INSERT,UPDATE ON hoge.* TO sousei@'localhost';
