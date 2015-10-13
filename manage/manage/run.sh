sudo nginx -s reload
killall -9 uwsgi
uwsgi -x uwsgi.xml --daemonize uwsgi.log
tail -F uwsgi.log
