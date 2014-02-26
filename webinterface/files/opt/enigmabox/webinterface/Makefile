all:
	clear
	./manage.py syncdb
	./manage.py migrate app
	./manage.py runserver

trans:
	./manage.py makemessages -a

compiletrans:
	./manage.py compilemessages

.PHONY: all
