#cd /var/flask_app && uwsgi_python3 --ini uwsgi.ini & nginx -g "daemon off;"
cd /var/flaskapp
python3 run.py -mb
uwsgi_python3 --ini uwsgi.ini & 
nginx -g "daemon off;" 
#nginx -g "daemon off;"
#python3 run.py -mb
/bin/bash
#cd /var/flask_app
#python3 run.py
# GRANT SELECT,INSERT,UPDATE ON hoge.* TO sousei@'localhost';

