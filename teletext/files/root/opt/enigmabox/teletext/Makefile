all:
	clear
	#./teletext.py
	sudo -u www-data gunicorn --bind=127.0.0.1:8008 --worker-class=gevent_pywsgi --workers=1 --debug --log-level=debug teletext:app

.PHONY: all
